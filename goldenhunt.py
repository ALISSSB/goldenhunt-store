import streamlit as st
import requests
import json
import pandas as pd
import stripe # type: ignore
from datetime import datetime
import os

# إعداد Stripe
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

# صفحة Streamlit
st.set_page_config(page_title="GoldenHunt 🛒", layout="wide")

# قائمة الطلبات
ORDERS_FILE = "orders.json"

def save_order(product_name, quantity, price):
    order = {
        "product_name": product_name,
        "quantity": quantity,
        "total_price": quantity * price,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = json.load(f)
    else:
        orders = []

    orders.append(order)

    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

def create_checkout_session(product_name, price, quantity):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product_name},
                'unit_amount': int(price * 100),
            },
            'quantity': quantity,
        }],
        mode='payment',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )
    return session.url

# الواجهة الرئيسية
def main():
    st.sidebar.title("GoldenHunt 🛒")
    menu = st.sidebar.radio("📋 القائمة:", ["🛒 متجر المنتجات", "📈 لوحة التحكم"])

    if menu == "🛒 متجر المنتجات":
        st.title("🔥 المنتجات المتوفرة:")
        products = [
            {"name": "سماعات بلوتوث", "price": 29.99},
            {"name": "ساعة ذكية", "price": 49.99},
            {"name": "شاحن متنقل", "price": 19.99}
        ]

        for i, product in enumerate(products):
            with st.container(border=True):
                st.subheader(f"{product['name']}")
                st.write(f"💸 السعر: {product['price']}$")

                quantity = st.number_input(f"حدد الكمية لـ {product['name']}:", min_value=1, step=1, key=f"qty_{i}")

                if st.button(f"✅ اطلب الآن - {product['name']}", key=f"order_{i}"):
                    payment_link = create_checkout_session(product['name'], product['price'], quantity)
                    save_order(product['name'], quantity, product['price'])
                    st.success("✅ تم تسجيل طلبك، انتقل للدفع عبر Stripe!")
                    st.markdown(f"[💳 ادفع الآن عبر Stripe]({payment_link})", unsafe_allow_html=True)

    elif menu == "📈 لوحة التحكم":
        st.title("📊 لوحة تحكم الطلبات")

        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                orders = json.load(f)

            df = pd.DataFrame(orders)

            if not df.empty:
                st.write("📝 جدول الطلبات:")
                st.dataframe(df)

                total_sales = df['total_price'].sum()
                st.metric("💰 إجمالي الأرباح:", f"${total_sales:.2f}")

                most_ordered = df['product_name'].value_counts()
                st.bar_chart(most_ordered)

                df['date'] = pd.to_datetime(df['date'])
                df_grouped = df.groupby(df['date'].dt.date).sum(numeric_only=True)
                st.line_chart(df_grouped['total_price'])
            else:
                st.info("لا توجد طلبات بعد!")
        else:
            st.info("📭 لم يتم تسجيل أي طلبات حتى الآن.")

if __name__ == "__main__":
    main()

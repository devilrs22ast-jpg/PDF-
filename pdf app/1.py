# Replace with your actual FamPay UPI ID and Name
upi_id = "9596900705@fam" 
name = "Raghav Sharma"

# The standard format for a UPI deep link
upi_link = f"upi://pay?pa={upi_id}&pn={name}&cu=INR"

st.sidebar.markdown("---")
st.sidebar.write("Support my work! ☕")
# We use HTML here because standard Markdown sometimes blocks upi:// links
st.sidebar.markdown(f'<a href="{upi_link}"><b>Tap here to Pay via UPI</b></a>', unsafe_allow_html=True)

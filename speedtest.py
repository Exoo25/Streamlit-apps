import streamlit as st
import speedtest

st.set_page_config(layout="wide")  # Set wide layout for side-by-side view
st.title("🚀 Internet Speed Test")

# Store last test results
if "last_result" not in st.session_state:
    st.session_state.last_result = {"Download": 0, "Upload": 0, "Ping": 0}

def check_speed():
    with st.spinner("Testing... Please wait..."):
        stest = speedtest.Speedtest()
        stest.get_best_server()

        download_speed = stest.download() / 1_000_000  # Convert to Mbps
        upload_speed = stest.upload() / 1_000_000  # Convert to Mbps
        ping = stest.results.ping

    return download_speed, upload_speed, ping

# Layout: Left for Results, Right for Chart
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Start Test", key="start_test"):
        download, upload, ping = check_speed()

        # Store latest result
        st.session_state.last_result = {
            "Download": round(download, 2),
            "Upload": round(upload, 2),
            "Ping": round(ping, 2)
        }

    st.success("✅ Speed Test Completed!")
    st.metric("Download Speed", f"{st.session_state.last_result['Download']} Mbps")
    st.metric("Upload Speed", f"{st.session_state.last_result['Upload']} Mbps")
    st.metric("Ping", f"{st.session_state.last_result['Ping']} ms")

with col2:
    st.subheader("📊 Speed Test Donut Chart")
    
    # Google Charts Donut Chart HTML
    donut_chart_data = [["Type", "Speed (Mbps)"], 
                        ["Download Speed", st.session_state.last_result["Download"]], 
                        ["Upload Speed", st.session_state.last_result["Upload"]], 
                        ["Ping (ms)", st.session_state.last_result["Ping"]]]
    
    chart_html = f"""
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        google.charts.load("current", {{"packages":["corechart"]}});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {{
            var data = google.visualization.arrayToDataTable({donut_chart_data});
            var options = {{
                title: 'Internet Speed Results',
                pieHole: 0.4,
                backgroundColor: '#f9f9f9',
                slices: {{ 0: {{ color: '#4285F4' }}, 1: {{ color: '#34A853' }}, 2: {{ color: '#FBBC05' }} }},
                legend: {{ position: 'right' }}
            }};
            var chart = new google.visualization.PieChart(document.getElementById('donut_chart'));
            chart.draw(data, options);
        }}
    </script>
    <div id="donut_chart" style="width: 100%; height: 500px;"></div>
    """
    
    st.components.v1.html(chart_html, height=550)

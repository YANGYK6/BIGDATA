import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

def visualize():
    # 创建图表对象
    fig = go.Figure()
    # 读取数据
    df = pd.read_csv("cpi_data.csv")
    df.columns = ['Date', 'Value']
    df['Date'] = pd.to_datetime(df['Date'])
    # print(df)
    # 添加主折线
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Value'],
        mode='lines+markers+text',
        name='CPI',
        line=dict(color='royalblue', width=4),
        marker=dict(size=10, color='rgba(0,0,128,0.8)', line=dict(width=1, color='white')),
        hovertemplate='日期: %{x|%Y-%m-%d}<br>CPI值: %{y:.4f}<extra></extra>'
    ))

    # 添加背景色和美化网格
    fig.update_layout(
        title=dict(text='📈 CPI 指数变化趋势图', x=0.5, font=dict(size=26)),
        xaxis=dict(
            title='日期',
            tickformat='%Y-%m-%d',
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)',
            linecolor='gray'
        ),
        yaxis=dict(
            title='CPI 值',
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)',
            linecolor='gray'
        ),
        plot_bgcolor='rgba(245,245,255,1)',
        paper_bgcolor='rgba(240,240,255,1)',
        hovermode='x unified',
        margin=dict(l=60, r=40, t=100, b=80),
        font=dict(family='"Microsoft YaHei", Arial', size=14),
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01)
    )

    # 添加图表脚注
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0, y=-0.25,
        showarrow=False,
        font=dict(size=12, color="gray")
    )
    pio.write_images(fig, 'cpi_trend.png',width=1800, height=1200)
    # 保存为HTML并打开
    fig.write_html("cpi_trend.html", auto_open=True)


if __name__ == '__main__':
    visualize()

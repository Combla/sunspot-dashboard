import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['YEAR'] = df['YEAR'].astype(int)
    df['DATE'] = pd.to_datetime(df['YEAR'].astype(str), format='%Y')
    df.set_index('DATE', inplace=True)
    return df

def plot_advanced_sunspot_visualizations(df, sunactivity_col='SUNACTIVITY'):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("Sunspots Data Advanced Visualization", fontsize=18)

    # 시계열 그래프
    axs[0, 0].plot(df.index, df[sunactivity_col], color='blue')
    axs[0, 0].set_title("Sunspot Activity Over Time")
    axs[0, 0].set_xlabel("Year")
    axs[0, 0].set_ylabel("Sunspot Count")
    axs[0, 0].grid(True)

    # 분포 그래프
    data = df[sunactivity_col].dropna().values
    xs = np.linspace(data.min(), data.max(), 200)
    density = gaussian_kde(data)
    axs[0, 1].hist(data, bins=30, density=True, alpha=0.6, color='gray', label='Histogram')
    axs[0, 1].plot(xs, density(xs), color='red', linewidth=2, label='Density')
    axs[0, 1].set_title("Distribution of Sunspot Activity")
    axs[0, 1].set_xlabel("Sunspot Count")
    axs[0, 1].set_ylabel("Density")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # 상자 그림
    df_20th = df.loc["1900":"2000"]
    axs[1, 0].boxplot(df_20th[sunactivity_col], vert=False)
    axs[1, 0].set_title("Boxplot of Sunspot Activity (1900-2000)")
    axs[1, 0].set_xlabel("Sunspot Count")

    # 산점도 + 추세선
    years = df["YEAR"].values
    sunspots = df[sunactivity_col].values
    mask = ~np.isnan(sunspots)
    years, sunspots = years[mask], sunspots[mask]
    axs[1, 1].scatter(years, sunspots, s=10, alpha=0.5, color='skyblue', label='Data Points')
    coef = np.polyfit(years, sunspots, 1)
    trend = np.poly1d(coef)
    axs[1, 1].plot(years, trend(years), color='red', linewidth=2, label='Trend Line')
    axs[1, 1].set_title("Trend of Sunspot Activity")
    axs[1, 1].set_xlabel("Year")
    axs[1, 1].set_ylabel("Sunspot Count")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

st.title('🌞 태양흑점 데이터 분석 대시보드 🌞')

try:
    df = load_data("data/sunspots.csv")
    st.subheader('📊 시각화 결과')
    fig = plot_advanced_sunspot_visualizations(df)
    st.pyplot(fig)
except Exception as e:
    st.error(f"오류 발생: {e}")

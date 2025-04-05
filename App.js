import React, { useState, useEffect } from "react";
import Chart from "chart.js";

// API მოთხოვნა Flask backend-ს
const fetchMarketSignal = async () => {
  const response = await fetch("/api/market_signal");
  const data = await response.json();
  return data;
};

const App = () => {
  const [signal, setSignal] = useState("");
  const [marketValue, setMarketValue] = useState(0);
  const [rsi, setRsi] = useState(null);
  const [macd, setMacd] = useState(null);
  const [chartData, setChartData] = useState([]);

  const updateChart = (data) => {
    const ctx = document.getElementById("myChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: data.map((item) => item.time),
        datasets: [
          {
            label: "Market Value",
            data: data.map((item) => item.value),
            borderColor: "rgb(75, 192, 192)",
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: {
            type: "time",
          },
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      const marketData = await fetchMarketSignal();
      setSignal(marketData.signal);
      setMarketValue(marketData.market_value);
      setRsi(marketData.rsi);
      setMacd(marketData.macd);

      // ცოცხალი მონაცემების განახლება ჩარტში
      const newChartData = [
        ...chartData,
        { time: new Date(), value: marketData.market_value },
      ];
      setChartData(newChartData);
      updateChart(newChartData); // განახლება ჩარტის მონაცემებით
    }, 10000); // ყოველ 10 წამში ბაზრის სიგნალი

    return () => clearInterval(interval);
  }, [chartData]);

  return (
    <div className="container">
      <header>
        <h1>Trading Bot Dashboard</h1>
      </header>
      <div className="signal">
        <h2>Market Signal: {signal}</h2>
        <p>Current Market Value: ${marketValue.toFixed(2)}</p>
        {rsi && <p>RSI: {rsi.toFixed(2)}</p>}
        {macd && <p>MACD: {macd.toFixed(2)}</p>}
      </div>
      <div className="chart">
        <canvas id="myChart"></canvas>
      </div>
    </div>
  );
};

export default App;

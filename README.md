# 應用生成式 AI 結合 6E 教學模式與自我決定理論對高中生 STEM 學習之影響研究

本儲存庫包含專為碩士論文設計的實驗數據生成模型、統計分析腳本及預期結果可視化工具。本研究旨在探討生成式 AI 介入教學對高中生在 **STEM 學習動機**與**認知負荷**之影響。

---

## 📝 專案概述 (Project Overview)

本研究採用準實驗設計（Quasi-experimental Design），探討生成式 AI 在高中生活科技課程中的應用成效。研究整合以下理論框架：
* **教學模式**：6E 教學法 (Engage, Explore, Explain, Engineer, Enrich, Evaluate)。
* **心理理論**：自我決定理論 (Self-Determination Theory, SDT)。
* **核心工具**：生成式 AI (Generative AI) 作為學習支架，協助學生進行實作與問題解決。

本專案模擬了 **$N=106$** 名受試者的實驗數據，分為實驗組（Experimental Group, $n=53$）與控制組（Control Group, $n=53$）。

## 📊 研究工具與維度 (Instruments)

研究採用兩套標準化量表進行前後測評量：

| 量表名稱 | 題數 | 維度內容 | 計分方式 |
| :--- | :--- | :--- | :--- |
| **學習動機量表** | 34 | 內在動機、勝任感、自主感、關係感 | Likert 5 點 |
| **認知負荷量表** | 10 | 內在負荷 (IL)、外在負荷 (EL)、增生負荷 (GL) | 0-10 分 |

## 🚀 技術架構 (Technical Stack)

本專案分析流程參考學姊之研究架構進行開發：
* **數據生成**：利用 `NumPy` 模擬具備學術統計邏輯的受試者填答數據。
* **統計分析**：使用 `statsmodels` 執行 **線性混合模型 (MixedLM)** 與 **共變數分析 (ANCOVA)**。
* **可視化**：透過 `Plotly` 產出交互式趨勢折線圖，展現前後測之交互作用。
* **論文整合**：自動生成符合學術規範（booktabs）的 LaTeX 統計表格代碼。

## 📦 檔案結構 (Repository Structure)

* `generate_fake_data.py`: 模擬受試者原始填答行為，產出具備題項級數據的 CSV 檔。
* `analysis.py`: 核心分析程式，執行統計檢定並產出圖表與 LaTeX 代碼。
* `data_wide.csv`: 寬格式數據，

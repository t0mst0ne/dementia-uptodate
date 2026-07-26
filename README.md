# 🧠 Dementia & Alzheimer's Disease — Weekly Trend Report

> 自動彙整失智症 / 阿茲海默症相關的最新研究、臨床試驗、藥物核准動態，每週發布至 GitHub Wiki。

---

## 📌 目前主題

**失智症 / 阿茲海默症（Dementia / Alzheimer's Disease）**

涵蓋：
- Amyloid 標靶治療（lecanemab、donanemab、aducanumab...）
- Tau 標靶治療
- Cholinesterase inhibitors & memantine
- 血液/影像 biomarker（plasma p-tau217、amyloid PET、tau PET）
- 輕度認知障礙（MCI）進展追蹤
- AAIC、CTAD、AAN 等重要會議摘要

---

## 🚀 功能

- **自動爬取**：Alzforum、NEJM、JAMA Neurology、Alzheimer's Association、CTAD 等來源
- **關鍵字篩選**：依 `source/keywords.yml` 過濾相關文章
- **藥物分群**：依 `source/drug_groups.yml` 自動分類新聞
- **AI 摘要**：使用 Claude API 產生中文摘要報告
- **自動發布**：每週透過 GitHub Actions 更新 Wiki

---

## 📁 專案結構

```
.
├── source/
│   ├── keywords.yml        # 失智症關鍵字列表
│   ├── drug_groups.yml     # 藥物分群設定
│   ├── search_queries.yml  # Twitter/X 搜尋 query
│   └── web_sources.yml     # RSS / Google News 來源
├── config/
│   └── seeds.txt           # KOL Twitter 帳號列表
├── src/
│   ├── webscraper.py       # 網頁爬蟲
│   ├── reporter.py         # AI 摘要產生器
│   └── wiki_publisher.py   # Wiki 發布器
├── reports/                # 產生的週報（Markdown）
├── .github/workflows/      # GitHub Actions CI/CD
└── main.py                 # 主程式入口
```

---

## ⚙️ 設定

### 1. 必要的 GitHub Secrets

| Secret 名稱 | 說明 |
|------------|------|
| `TWITTER_USERNAME` | X/Twitter username（不含 @） |
| `TWITTER_EMAIL` | X/Twitter account email |
| `TWITTER_AUTH_TOKEN` | X/Twitter `auth_token` cookie |
| `TWITTER_CT0` | X/Twitter `ct0` cookie |

### 2. 修改資料來源

編輯 `source/web_sources.yml` 新增或移除網站來源。

### 3. 修改關鍵字

編輯 `source/keywords.yml` 調整過濾條件。

---

## 🔄 執行方式

### 手動執行

```bash
pip install -r requirements.txt
python main.py
```

### 自動排程

GitHub Actions 每週一 UTC 00:00 自動執行，結果提交至 `reports/`，再由 Wiki workflow 發布至本 repo 的 **Wiki**。

首次啟用前，請在 GitHub repository settings → Secrets and variables → Actions
新增上述四個 secrets，並先初始化 repository Wiki。

---

## 📊 報告範例

每份週報包含：
- 本週重點新聞摘要（中文）
- 依藥物分類的試驗進展
- 新藥核准 / FDA 動態
- 重要會議（AAIC / CTAD / AAN）摘要

---

## 🔗 相關資源

- [Alzforum](https://www.alzforum.org/)
- [Alzheimer's Association](https://www.alz.org/)
- [ClinicalTrials.gov — Dementia](https://clinicaltrials.gov/search?cond=Dementia)
- [AAIC](https://aaic.alz.org/)
- [CTAD](https://www.ctad-alzheimer.com/)

---

## 📝 License

MIT License — 本專案為學術與臨床教育用途。

---

> 原始專案：[htlin222/breast-cancer-uptodate](https://github.com/htlin222/breast-cancer-uptodate)
> 改編版本：失智症主題

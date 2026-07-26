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

- **網頁新聞爬取**：Alzforum、NeurologyToday、Alzheimer's Association、CTAD/AAIC，
  以及 NEJM / JAMA Neurology 的 Google News RSS，只收最近 7 天
- **期刊文獻**：透過 CrossRef API 抓取 Alzheimer's & Dementia、Lancet Neurology、
  JAMA Neurology、Neurology、Alzheimer's Research & Therapy、NEJM，預設 14 天
- **兩層關鍵字篩選**：依 `source/keywords.yml` 與 `src/crossref_fetcher.py` 的
  Tier-1/Tier-2 詞庫過濾，排除心臟類澱粉沉積症、腫瘤等他科文獻
- **Telegram 通知**：產生新報告後自動推播
- **自動發布**：每週透過 GitHub Actions 提交報告並更新 Wiki

> 註：報告內容的中文撰寫由 Claude Code 依 `CLAUDE.md` 的規範在對話中完成，
> pipeline 本身只負責蒐集素材並產生原始清單。

---

## 📁 專案結構

```
.
├── source/
│   ├── keywords.yml        # 失智症關鍵字列表
│   ├── journals.yml        # CrossRef 期刊來源（ISSN）
│   ├── web_sources.yml     # RSS / Google News 來源
│   ├── drug_groups.yml     # 藥物分群設定
│   ├── search_queries.yml  # 保留的歷史設定
│   ├── twitter.yml         # 保留的歷史設定（已停用）
│   └── MIGRATION_GUIDE.md  # 乳癌 → 失智症的歷史遷移紀錄
├── src/
│   ├── config.py           # YAML 設定載入 + 關鍵字比對
│   ├── webscraper.py       # 網頁新聞爬蟲（含日期過濾）
│   ├── crossref_fetcher.py # CrossRef 期刊擷取 + 兩層預篩
│   └── telegram_notifier.py# Telegram Bot 推播
├── data/                   # 擷取結果快取（JSON）
├── reports/                # 產生的週報（Markdown）
├── .github/workflows/      # GitHub Actions CI/CD
└── main.py                 # 主程式入口
```

`src/` 另有 `reporter.py`、`db.py`、`discover.py`、`fetcher.py`，是乳癌時期的遺留
程式，目前未被 pipeline 引用。

---

## ⚙️ 設定

### 1. GitHub Secrets

蒐集來源全部為公開的 RSS / Google News / CrossRef，**不需要金鑰**。
只有 Telegram 通知需要以下兩個 secret，未設定時該步驟會自動跳過而非失敗：

| Secret 名稱 | 說明 |
|------------|------|
| `TELEGRAM_BOT_TOKEN` | 向 [@BotFather](https://t.me/BotFather) 申請 bot 後取得 |
| `TELEGRAM_CHAT_ID` | 與 bot 對話後，從 `https://api.telegram.org/bot<TOKEN>/getUpdates` 的 `message.chat.id` 取得（注意不是 bot 自己的 id） |

### 2. 修改資料來源

- 網頁新聞：編輯 `source/web_sources.yml`
- 期刊：編輯 `source/journals.yml`，填入 ISSN（可於 https://portal.issn.org 查詢）

### 3. 修改關鍵字

編輯 `source/keywords.yml` 調整過濾條件。

---

## 🔄 執行方式

本專案使用 [uv](https://docs.astral.sh/uv/) 管理相依套件。

```bash
uv sync                        # 安裝相依套件

uv run python main.py scrape   # 只抓網頁新聞
uv run python main.py journals # 只抓期刊文獻
uv run python main.py run      # 完整流程並寫出報告
uv run python main.py notify   # 推播最新報告至 Telegram
```

### 自動排程

GitHub Actions 每週一 UTC 00:00（台北時間週一 08:00）自動執行，
結果提交至 `reports/`，推播 Telegram，再由 Wiki workflow 發布至本 repo 的 **Wiki**。

首次啟用前，請先初始化 repository Wiki。

> ⚠️ Action 以 UTC 計算 ISO 週數。若在台北時間週日晚間手動觸發，
> 會產生屬於**上一週**的檔案，內容與當週報告重複。

---

## 🔍 資料篩選邏輯

兩個容易踩到的陷阱，修改程式前請先理解：

**1. 關鍵字採字界比對，不可用子字串包含。**
`source/keywords.yml` 含 `AD`、`tau`、`MCI`、`NIA` 等短縮寫。若用 `kw in text`，
`AD` 會命中 "r*ad*iotherapy"、`tau` 會命中 "pla*tau*"，導致他科論文被誤標。
請一律使用 `config.match_keywords()` / `config.keyword_pattern()`。

**2. CrossRef 預篩是兩層架構**（`src/crossref_fetcher.py`）。
Tier 1 為無歧義詞（`dementia`、`Alzheimer`、`lecanemab`、`p-tau217`…），單獨出現即通過；
Tier 2 為跨領域共用詞（`amyloid`、`tau`、`biomarker`、`cognition`），單獨出現一律不通過，
因為心臟類澱粉沉積症與腫瘤激酶論文同樣會使用這些詞。

Python 端的篩選只是廣撒網。撰寫報告時仍須讀取 `data/journals_cache.json`
並逐篇確認主題確實為失智症，再放進 `## 文獻速報`。

---

## 🔀 切換至其他主題

以帕金森氏症為例，四個步驟：

1. **`source/keywords.yml`** — 將 `dementia_keywords:` 底下的詞替換為新主題
   （疾病名、生物標記、藥物、試驗、會議）。
2. **`source/web_sources.yml`** — 替換 RSS 與 Google News 的網域與查詢字串。
3. **`source/journals.yml`** — 替換期刊 ISSN。建議先驗證：
   ```bash
   curl -s https://api.crossref.org/journals/<ISSN> | head -c 300
   ```
4. **`src/crossref_fetcher.py`** — 更新 `_DEMENTIA_DIRECT` 與 `_SHARED_TERMS`。
   **這步最容易被遺漏**：詞庫寫死在程式碼裡，只改 YAML 不會生效，
   舊詞庫會靜默放行他科論文（本專案曾因此讓乳癌放療與膠質母細胞瘤試驗混入失智症週報）。

最後更新 `CLAUDE.md` 的章節結構、試驗名稱與療效指標。
`source/MIGRATION_GUIDE.md` 記錄了乳癌 → 失智症那次遷移的細節，可供參考。

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

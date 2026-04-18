# 切換至失智症的程式碼修改說明

## 1. `main.py` — 報告標題

搜尋所有含 "breast cancer" 或 "Breast Cancer" 的字串，替換為：

```python
# 舊
"Breast Cancer Weekly Trend Report"
# 新
"Dementia & Alzheimer's Disease Weekly Trend Report"
```

如果有 scrape 指令的 topic 參數，也一併修改：
```python
# 舊
topic = "breast cancer"
# 新
topic = "dementia Alzheimer"
```

---

## 2. `src/reporter.py` — 報告標題與 prompt

搜尋含 "乳癌" 或 "breast cancer" 的字串，替換為：

```python
# 舊
"乳癌（Breast Cancer）每週治療趨勢報告"
# 新
"失智症（Dementia / Alzheimer's Disease）每週治療趨勢報告"
```

如有 Claude / AI prompt 中的 system message 說明癌種，也替換：
```
# 舊
你是一位腫瘤科（乳癌）的醫療資訊整合助理 ...
# 新
你是一位神經科（失智症 / Alzheimer's disease）的醫療資訊整合助理，
專注於失智症治療趨勢、新藥核准、臨床試驗進展，
以及 amyloid、tau、biomarker 相關研究。
```

---

## 3. `src/webscraper.py` — Google News 預設 query

找到這一行（約在 `_fetch_google_news` 函式中）：

```python
query_term = src.get("query", "breast cancer")
```

替換為：

```python
query_term = src.get("query", "Alzheimer dementia")
```

---

## 4. README.md — 描述更新

```markdown
# 舊
目前設定：**乳癌（Breast Cancer）**
資料來源：OpenEvidence AI · OncDaily RSS · OncLive · ESMO · ClinicalTrials.gov

# 新
目前設定：**失智症 / 阿茲海默症（Dementia / Alzheimer's Disease）**
資料來源：Alzforum · NEJM · JAMA Neurology · Alzheimer's Association · CTAD · ClinicalTrials.gov
```

---

## 摘要：需要修改的位置

| 檔案 | 修改內容 |
|------|---------|
| `source/keywords.yml` | ✅ 已替換（見本 PR） |
| `source/drug_groups.yml` | ✅ 已替換（見本 PR） |
| `source/search_queries.yml` | ✅ 已替換（見本 PR） |
| `source/web_sources.yml` | ✅ 已替換（見本 PR） |
| `config/seeds.txt` | ✅ 已替換（見本 PR） |
| `src/webscraper.py` | 改一行 `query_term` 預設值 |
| `src/reporter.py` | 改標題字串與 AI prompt |
| `main.py` | 改標題字串與 topic 變數 |
| `README.md` | 改描述文字 |

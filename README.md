# 上下班路況 + 國道即時路況

## 檔案
- `index.html`:網頁(GitHub Pages)
- `route.json`:要監看的國道路段(依道路、方向、地名關鍵字篩選)
- `fetch_freeway.py`:抓取高公局路段即時路況
- `.github/workflows/freeway.yml`:通勤時段每約 10 分鐘自動執行
- `data/traffic.json`:抓取結果(由 Actions 自動更新)

## 啟用
1. 全部檔案依上述結構放進 repo(保留資料夾)。
2. Settings → Actions → General → Workflow permissions 選 **Read and write permissions**。
3. Actions → Freeway Traffic → Run workflow 手動執行一次,確認 `data/traffic.json` 有更新。
4. 若顯示「沒有符合的路段」,看頁面上列出的路段名稱範例,修改 `route.json` 的 keywords。

上場企業の財務データ分析をやってみる。

# 参考URL

- [EDINETガイド](https://disclosure.edinet-fsa.go.jp/EKW0EZ0015.html)
- [報告書インスタンス作成ガイドライン](https://disclosure.edinet-fsa.go.jp/download/ESE140159.pdf)
- [適時開示XBRLガイド](https://www.jpx.co.jp/equities/listing/xbrl/03.html)
- [Inline XBRL 1.0 specification](http://www.xbrl.org/specification/inlinexbrl-part1/rec-2010-04-20/inlinexbrl-part1-rec-2010-04-20+corrected-errata-2011-08-17.html)

# tdnet scraping info

```
- url -
[POST] https://www.release.tdnet.info/onsf/TDJFSearch/TDJFSearch

- headers -
Content-Type: application/x-www-form-urlencoded
Origin: https://www.release.tdnet.info
Referer: https://www.release.tdnet.info/onsf/TDJFSearch/I_head
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36

- body (x-www-form-urlencoded) -
t0:20190403
t1:20190403
q:短信
m:0
```
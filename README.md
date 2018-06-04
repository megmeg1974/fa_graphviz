# fa_graphviz
有限状態機械(finite automaton)の状態遷移図を**graphviz**で作成するときに使用するツール。

※まだまだ、作りかけです。



## 使用例

1. FA定義(入力ファイル)

```bash
$ cat sample/sample_fa.txt
title:sample_fa

# 正常系
start -> q0 -1-> r1 -1-> r2 -0-> r3 -0-> t[F]

# ドボン
q0 -0-> s
r1 -0-> s

# ドボンのループ
s -0,1-> s

# 途中のループ
r2 -1-> r2
r3 -1-> r2
t -1-> r2
t -0-> t
```
2. 上記のFA定義から**graphviz**の入力テキストを出力する。
```bash
$ ./fa.py sample/sample_fa.txt
digraph G {
  graph [charset="UTF-8"];
  rankdir=LR;
  label="sample_fa";

  start    -> q0
  q0       -> r1       [label="1"];
  r1       -> r2       [label="1"];
  r2       -> r3       [label="0"];
  r3       -> t        [label="0"];
  q0       -> s        [label="0"];
  r1       -> s        [label="0"];
  s        -> s        [label="0,1"];
  r2       -> r2       [label="1"];
  r3       -> r2       [label="1"];
  t        -> r2       [label="1"];
  t        -> t        [label="0"];
  t        [shape=doublecircle rank=max];
  start    [shape=none rank=max];
}
```
3. 上記のテキストを **graphviz**で処理すると、下記グラフが生成される。

![](http://g.gravizo.com/g?  digraph G {    graph [charset="UTF-8"];    rankdir=LR;    label="sample_fa";    start    -> q0    q0       -> r1       [label="1"];    r1       -> r2       [label="1"];    r2       -> r3       [label="0"];    r3       -> t        [label="0"];    q0       -> s        [label="0"];    r1       -> s        [label="0"];    s        -> s        [label="0,1"];    r2       -> r2       [label="1"];    r3       -> r2       [label="1"];    t        -> r2       [label="1"];    t        -> t        [label="0"];    t        [shape=doublecircle rank=max];    start    [shape=none rank=max];  })



## FA定義の書き方



| 項目            | 書式                    | 記述例             | 説明                    |
| --------------- | ----------------------- | ------------------ | ----------------------- |
| タイトル定義    | `title:【タイトル名】`  |`title:sample_fa`   | グラフにつけるラベル    |
| ノード間の遷移  | `【遷移元ノード】-【入力記号】->【遷移先ノード】` | `n1-1,2->n2` | 【ノード1】(`n1`)で入力記号(`1`または`2`)を受けると【ノード2】(`n2`)に遷移する。 |
| 初期状態        | `start -> 【初期状態】` | `start -> q0`      | 初期状態ノードは`start`の遷移先として記述する。|
| 終了状態        | `【終了状態】[F]`       | `r3 -0-> t[F]`     | 終了状態のノードには[F]をつける。 |
| コメント        | `# 【コメント文字列】   | `# ここはコメント` | `#`始まりの行はコメント |


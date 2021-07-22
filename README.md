# OCR 文字認識
<div style="text-align: right;">
 03-210245 峰岸剛基
</div>

## 概要
人間が書いた文字特に日本語を機械に認識させたい。
## 動機
IPad OS 14で導入されたスクリブルという手書きの文字をかなりの精度で認識する機能がある。  下のように検索窓にApple pencil で書いた文字を検索できる。  

<img src="image1.png" width="270"><img src="image2.png" width="270">  
しかしまだ日本語対応していなく不便。だから自分で実装。  

## 調査
調べてわかったこととして機械学習(Deep learning)を用いる必要があるということ。それには学習用の大量のデータが必要であるということ。

## データ
[ETLデータベース](http://etlcdb.db.aist.go.jp/obtaining-etl-character-database?lang=ja)  
　
ひらがなと濁点と半濁点の合計48文字を認識する。漢字は多すぎて大変。
謎の拡張子だったのでpngに変換。64*64pixelとか。

<img src="image3.png" width="270"><img src="image5.png" width="270">

## 文字認識
学習にGPUを使わないと時間かかるので無料でGPUが使えるGoogle colabで行った。学習後の重みファイルのみロードして実際に自分で書いた文字を予測する。 
![](nagare.png)  
画像認識として精度のたかいResnet18を使用。  
18は層の数を示す。  
ディープラーニングでは基本的に層の数が多いほど複雑なものを表せるが今回二値化しているため18くらいでいいかと。あとcolabのGPUも多分12GBくらいしか使えないので、軽いモデルを選択した。  
工夫した点は二値化したことと、Earlystopping　で過学習を防止した。
![](model.png)  
学習結果が以下
![](learning.png)
validationのaccuracyが95％くらいでした。
  

## 結果
データ IPadで書いた文字をスクショして切り取ったもの。

<img src="さ_1_Ipad.jpg" width="150">

出力
```
python predict.py 画像のpath
```

で画像のひらがながなにか予測

<img src="image6.png" width="270">

「さ」が認識できた！  

ちなみに他の文字や文字を太くしてもいけそう。  

<img src="あ_Ipad.jpg" width="270"><img src="image8.png" width="270">

## 反省
- 筆の太さがGood note の一番細いやつだとうまくできない。

<img src="Ipad_さ.jpg" width="270"><img src="image7.png" width="270">  

- 精度が低い   
以下は「あ、い、う、え、お」をそれぞれ予測させた結果である。  
「え」が「ん」に認識されている。確かに似ているけど区別してほしかった。
<img src="aiueo.png" width="270">  

- 複数の文字をは無理  
授業でもやったがopencvで微分とかして輪郭求めようとしてもしたの画像のようになってしまう。文字の位置を認識するモデルも必要みたい。  

<img src="aiueo_detection.jpg" width="270">  

- IPad OS 15でスクリブルが日本語対応してしまうらしい
- もっとみんなみたいにかっこいいわかりやすいUIを作って「すごい」って思われたかった。

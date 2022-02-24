# japanese2phoneme

A python library to convert Japanese to phoneme.

## Install

```
pip install japanese2phoneme
```

## Quick Start

```
>>> import japanese2phoneme
>>> japanese2phoneme.get_chunked_kana('林檎')
(['林檎'], ['リンゴ'], ['r i ɴ g o'])
>>> japanese2phoneme.get_chunked_kana('リンゴ')
(['リンゴ'], ['リンゴ'], ['r i ɴ g o'])
>>> japanese2phoneme.get_chunked_kana('これは牡蠣です')
(['これは牡蠣です'], ['コレハカキデス'], ['k o r e h a k a k i d e s u'])
>>> japanese2phoneme.get_chunked_kana('これは柿です')
(['これは柿です'], ['コレハカキデス'], ['k o r e h a k a k i d e s u'])
```

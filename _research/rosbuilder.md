---
number: '03'
title: ROS 2ノード設計ツール ROSBuilder
description: モジュールの仕様から、ROS 2ノードの雛形等を自動生成し、開発の立ち上げを支援。
stages:
- develop
icon: code
owners:
- 産業技術総合研究所
- 名城大学
owner_short: 産業技術総合研究所・名城大学
featured: true
resource_url: https://github.com/OpenRTM/OpenRTP-aist/releases/tag/v2.1.0
---
## 仕様からコードへ、開発の入口をつなぐ
ROSBuilderは、モジュールの仕様を入力し、ROS 2ノードの開発に必要な成果物を自動生成する設計ツールです。繰り返し行う雛形作成を支援し、モジュール固有の機能開発に取り組みやすい環境を目指します。

## 主な研究開発内容
- C++・Python等のROSノード雛形の生成
- プロファイル、マニフェストなどの生成
- ISO 22166-202に準拠したプロファイルの生成・読込み

## 活用を想定する場面
新しいROS 2モジュールを開発する際や、仕様と実装に関する情報を整理して引き渡す場面を支援します。

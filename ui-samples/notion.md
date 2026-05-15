# Design Style Guide: The AI workspace that works for you. | Notion

> Source: https://notion.so
> Extracted: 2026-05-15 16:41
> Viewport: 1280x720 | Full page height: 7228px

## Design Philosophy

- Mixed light/dark palette
- Dual typeface system: NotionInter, Lyon Text
- Pill-shaped elements (fully rounded corners)
- Glassmorphism / backdrop blur effects
- Generous whitespace with large section padding

---

## CSS Custom Properties

| Variable | Value |
|----------|-------|
| `--base-padding` | `60px` |
| `--border-color-regular` | `#00000014` |
| `--border-radius-0` | `0` |
| `--border-radius-200` | `0.25rem` |
| `--border-radius-300` | `0.3125rem` |
| `--border-radius-400` | `0.375rem` |
| `--border-radius-500` | `0.5rem` |
| `--border-radius-600` | `0.625rem` |
| `--border-radius-700` | `0.75rem` |
| `--border-radius-800` | `0.875rem` |
| `--border-radius-900` | `1rem` |
| `--border-radius-round` | `624.9375rem` |
| `--border-style-dashed` | `dashed` |
| `--border-style-none` | `none` |
| `--border-style-solid` | `solid` |
| `--border-width-1` | `0.0625rem` |
| `--border-width-2` | `0.125rem` |
| `--border-width-4` | `0.25rem` |
| `--color-alpha-black-100` | `#0000000d` |
| `--color-alpha-black-200` | `#0000001a` |
| `--color-alpha-black-300` | `#0003` |
| `--color-alpha-black-400` | `#0000004d` |
| `--color-alpha-black-500` | `#0000008a` |
| `--color-alpha-black-600` | `#00000096` |
| `--color-alpha-black-700` | `#000000bf` |
| `--color-alpha-black-800` | `#000000e6` |
| `--color-alpha-black-900` | `#000000f2` |
| `--color-alpha-white-100` | `#ffffff0d` |
| `--color-alpha-white-200` | `#ffffff1a` |
| `--color-alpha-white-300` | `#fff3` |
| `--color-alpha-white-400` | `#ffffff4d` |
| `--color-alpha-white-500` | `#ffffff80` |
| `--color-alpha-white-600` | `#ffffffa8` |
| `--color-alpha-white-700` | `#ffffffbf` |
| `--color-alpha-white-800` | `#ffffffd9` |
| `--color-alpha-white-900` | `#fffffff2` |
| `--color-black` | `#000` |
| `--color-blue-100` | `#f2f9ff` |
| `--color-blue-200` | `#e6f3fe` |
| `--color-blue-300` | `#93cdfe` |
| `--color-blue-400` | `#62aef0` |
| `--color-blue-500` | `#097fe8` |
| `--color-blue-600` | `#0075de` |
| `--color-blue-700` | `#005bab` |
| `--color-blue-800` | `#00396b` |
| `--color-blue-900` | `#002a4f` |
| `--color-brown-100` | `#fcf8f5` |
| `--color-brown-200` | `#ebd5c5` |
| `--color-brown-300` | `#d9b79f` |
| `--color-brown-400` | `#b18164` |
| `--color-brown-500` | `#9c7054` |
| `--color-brown-600` | `#885d3d` |
| `--color-brown-700` | `#744d2d` |
| `--color-brown-800` | `#654124` |
| `--color-brown-900` | `#523410` |
| `--color-campaigns-agents-launch-blue-300` | `#607df6` |
| `--color-campaigns-agents-launch-blue-400` | `#455dd3` |
| `--color-campaigns-agents-launch-blue-500` | `#394ea3` |
| `--color-campaigns-agents-launch-blue-600` | `#213183` |
| `--color-campaigns-agents-launch-blue-900` | `#02093a` |
| `--color-campaigns-agents-launch-yellow` | `#fefcd5` |
| `--color-campaigns-dev-platform-dos-alpha-blue` | `#1313baa8` |
| `--color-campaigns-dev-platform-dos-alpha-gray` | `#f6f6fc70` |
| `--color-campaigns-dev-platform-dos-alpha-lavender` | `#cbcbef70` |
| `--color-campaigns-dev-platform-dos-alpha-white` | `#ffffffbf` |
| `--color-campaigns-dev-platform-dos-black` | `#0a0a5d` |
| `--color-campaigns-dev-platform-dos-blue` | `#1313ba` |
| `--color-campaigns-dev-platform-dos-gray` | `#f6f6fc` |
| `--color-campaigns-dev-platform-dos-lavender` | `#cbcbef` |
| `--color-campaigns-dev-platform-dos-neon` | `#6666fd` |
| `--color-campaigns-dev-platform-dos-slate` | `#7171a8` |
| `--color-campaigns-dev-platform-dos-white` | `#fff` |
| `--color-gray-100` | `#f9f9f8` |
| `--color-gray-200` | `#f6f5f4` |
| `--color-gray-300` | `#dfdcd9` |
| `--color-gray-400` | `#a39e98` |
| `--color-gray-500` | `#78736f` |
| `--color-gray-600` | `#615d59` |
| `--color-gray-700` | `#494744` |
| `--color-gray-800` | `#31302e` |
| `--color-gray-900` | `#191918` |
| `--color-green-100` | `#f0faf2` |
| `--color-green-200` | `#d0f4d8` |
| `--color-green-300` | `#abe5b8` |
| `--color-green-400` | `#68ce7e` |
| `--color-green-500` | `#1aae39` |
| `--color-green-600` | `#14832b` |
| `--color-green-700` | `#0f6220` |
| `--color-green-800` | `#0a4216` |
| `--color-green-900` | `#05210b` |
| `--color-orange-100` | `#fff5ed` |
| `--color-orange-200` | `#ffdec4` |
| `--color-orange-300` | `#ffad71` |
| `--color-orange-400` | `#ff8a33` |
| `--color-orange-500` | `#ff6d00` |
| `--color-orange-600` | `#dd5b00` |
| `--color-orange-700` | `#ab4a00` |
| `--color-orange-800` | `#793400` |
| `--color-orange-900` | `#532200` |
| `--color-pink-100` | `#fff5fc` |
| `--color-pink-200` | `#ffcdf1` |
| `--color-pink-300` | `#ffb5eb` |
| `--color-pink-400` | `#ff83dd` |
| `--color-pink-500` | `#ff64c8` |
| `--color-pink-600` | `#d13f9d` |
| `--color-pink-700` | `#9d2472` |
| `--color-pink-800` | `#6c1b4f` |
| `--color-pink-900` | `#481034` |
| `--color-purple-100` | `#f8f5fc` |
| `--color-purple-200` | `#eadbfa` |
| `--color-purple-300` | `#d6b6f6` |
| `--color-purple-400` | `#ad6ded` |
| `--color-purple-500` | `#9849e8` |
| `--color-purple-600` | `#7237ae` |
| `--color-purple-700` | `#562983` |
| `--color-purple-800` | `#391c57` |
| `--color-purple-900` | `#1c0e2c` |
| `--color-red-100` | `#fef3f1` |
| `--color-red-200` | `#fdd3cd` |
| `--color-red-300` | `#ff8b7c` |
| `--color-red-400` | `#f77463` |
| `--color-red-500` | `#f64932` |
| `--color-red-600` | `#e32d14` |
| `--color-red-700` | `#b01601` |
| `--color-red-800` | `#6f0d00` |
| `--color-red-900` | `#4f0900` |
| `--color-teal-100` | `#f2fafa` |
| `--color-teal-200` | `#bde6e4` |
| `--color-teal-300` | `#83cbc9` |
| `--color-teal-400` | `#2a9d99` |
| `--color-teal-500` | `#27918d` |
| `--color-teal-600` | `#0a7b77` |
| `--color-teal-700` | `#126764` |
| `--color-teal-800` | `#0a4d4b` |
| `--color-teal-900` | `#042b29` |
| `--color-transparent` | `#fff0` |
| `--color-white` | `#fff` |
| `--color-yellow-100` | `#fff5e0` |
| `--color-yellow-200` | `#ffe4af` |
| `--color-yellow-300` | `#ffd786` |
| `--color-yellow-400` | `#ffc95e` |
| `--color-yellow-500` | `#ffb110` |
| `--color-yellow-600` | `#e89d01` |
| `--color-yellow-700` | `#c78600` |
| `--color-yellow-800` | `#a16c00` |
| `--color-yellow-900` | `#704b00` |
| `--decoration-link-underline-offset` | `0.1em` |
| `--decoration-link-underline-thickness` | `0.0625rem` |
| `--direction` | `1` |
| `--font-family-emoji` | `"Apple Color Emoji","Segoe UI Emoji",NotoColorEmoji,"Noto Color Emoji","Segoe UI Symbol","Android Emoji",EmojiSymbols` |
| `--font-family-fallback-emoji` | `"Segoe UI Emoji",NotoColorEmoji,"Noto Color Emoji","Segoe UI Symbol","Android Emoji",EmojiSymbols` |
| `--font-family-fallback-handwriting` | `-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-fallback-mono` | `Nitti,Menlo,Courier,monospace` |
| `--font-family-fallback-sans` | `Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-fallback-sans-arabic` | `NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-fallback-sans-hebrew` | `NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-fallback-sans-vietnamese` | `system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-fallback-serif` | `Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--font-family-fallback-serif-chinese-simplified` | `Georgia,"Songti TC",SimSun,serif` |
| `--font-family-fallback-serif-chinese-traditional` | `Georgia,"Songti SC",SimSun,serif` |
| `--font-family-fallback-serif-japanese` | `Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN",serif` |
| `--font-family-fallback-serif-vietnamese` | `"Times New Roman",serif` |
| `--font-family-handwriting` | `"Permanent Marker",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-mono` | `"iA Writer Mono",Nitti,Menlo,Courier,monospace` |
| `--font-family-primary-emoji` | `"Apple Color Emoji"` |
| `--font-family-primary-handwriting` | `"Permanent Marker"` |
| `--font-family-primary-mono` | `"iA Writer Mono"` |
| `--font-family-primary-sans` | `NotionInter` |
| `--font-family-primary-sans-arabic` | `"Noto Sans Arabic"` |
| `--font-family-primary-sans-hebrew` | `"Noto Sans Hebrew"` |
| `--font-family-primary-sans-vietnamese` | `ui-sans-serif` |
| `--font-family-primary-serif` | `"Lyon Text"` |
| `--font-family-primary-serif-chinese-simplified` | `"Lyon Text"` |
| `--font-family-primary-serif-chinese-traditional` | `"Lyon Text"` |
| `--font-family-primary-serif-japanese` | `"Lyon Text"` |
| `--font-family-primary-serif-vietnamese` | `ui-serif` |
| `--font-family-sans` | `NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-sans-arabic` | `"Noto Sans Arabic",NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-sans-hebrew` | `"Noto Sans Hebrew",NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-sans-vietnamese` | `ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--font-family-serif` | `"Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--font-family-serif-chinese-simplified` | `"Lyon Text",Georgia,"Songti TC",SimSun,serif` |
| `--font-family-serif-chinese-traditional` | `"Lyon Text",Georgia,"Songti SC",SimSun,serif` |
| `--font-family-serif-japanese` | `"Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN",serif` |
| `--font-family-serif-vietnamese` | `ui-serif,"Times New Roman",serif` |
| `--font-letter-spacing-mono-100` | `-0.0078125rem` |
| `--font-letter-spacing-sans-100` | `0` |
| `--font-letter-spacing-sans-1000-bold` | `-0.15625rem` |
| `--font-letter-spacing-sans-1000-regular` | `-0.25rem` |
| `--font-letter-spacing-sans-150` | `0` |
| `--font-letter-spacing-sans-200` | `0` |
| `--font-letter-spacing-sans-300` | `-0.0078125rem` |
| `--font-letter-spacing-sans-350` | `-0.0078125rem` |
| `--font-letter-spacing-sans-400` | `-0.015625rem` |
| `--font-letter-spacing-sans-50` | `0.0078125rem` |
| `--font-letter-spacing-sans-500` | `-0.0390625rem` |
| `--font-letter-spacing-sans-600-bold` | `-0.046875rem` |
| `--font-letter-spacing-sans-600-regular` | `-0.0625rem` |
| `--font-letter-spacing-sans-600-semibold` | `-0.046875rem` |
| `--font-letter-spacing-sans-700-bold` | `-0.09375rem` |
| `--font-letter-spacing-sans-700-regular` | `-0.125rem` |
| `--font-letter-spacing-sans-700-semibold` | `-0.09375rem` |
| `--font-letter-spacing-sans-800-bold` | `-0.1171875rem` |
| `--font-letter-spacing-sans-800-regular` | `-0.21875rem` |
| `--font-letter-spacing-sans-800-semibold` | `-0.1171875rem` |
| `--font-letter-spacing-sans-900-bold` | `-0.1328125rem` |
| `--font-letter-spacing-sans-900-regular` | `-0.171875rem` |
| `--font-letter-spacing-sans-900-semibold` | `-0.1328125rem` |
| `--font-letter-spacing-serif-200` | `0` |
| `--font-letter-spacing-serif-300` | `0` |
| `--font-letter-spacing-serif-350` | `0` |
| `--font-letter-spacing-serif-400` | `0` |
| `--font-letter-spacing-serif-500` | `0` |
| `--font-letter-spacing-serif-600` | `0` |
| `--font-letter-spacing-serif-700` | `-0.09375rem` |
| `--font-letter-spacing-serif-800` | `-0.125rem` |
| `--font-letter-spacing-serif-900` | `-0.125rem` |
| `--font-line-height-100` | `1.25rem` |
| `--font-line-height-1000` | `5rem` |
| `--font-line-height-150` | `1.25rem` |
| `--font-line-height-200` | `1.5rem` |
| `--font-line-height-300` | `1.75rem` |
| `--font-line-height-350` | `1.75rem` |
| `--font-line-height-400` | `1.75rem` |
| `--font-line-height-450` | `1.875rem` |
| `--font-line-height-50` | `1rem` |
| `--font-line-height-500` | `2rem` |
| `--font-line-height-600` | `2.5rem` |
| `--font-line-height-700` | `3rem` |
| `--font-line-height-800` | `3.5rem` |
| `--font-line-height-900` | `4rem` |
| `--font-size-100` | `0.875rem` |
| `--font-size-1000` | `4.75rem` |
| `--font-size-150` | `0.9375rem` |
| `--font-size-200` | `1rem` |
| `--font-size-300` | `1.125rem` |
| `--font-size-350` | `1.25rem` |
| `--font-size-400` | `1.375rem` |
| `--font-size-50` | `0.75rem` |
| `--font-size-500` | `1.625rem` |
| `--font-size-600` | `2rem` |
| `--font-size-700` | `2.625rem` |
| `--font-size-800` | `3.375rem` |
| `--font-size-900` | `4rem` |
| `--font-weight-bold` | `700` |
| `--font-weight-medium` | `500` |
| `--font-weight-regular` | `400` |
| `--font-weight-semibold` | `600` |
| `--font-weight-variable-bold` | `680` |
| `--font-weight-variable-medium` | `520` |
| `--font-weight-variable-regular` | `420` |
| `--font-weight-variable-semibold` | `620` |
| `--global-navigation-height` | `64px` |
| `--grid-column-width` | `1fr` |
| `--grid-columns` | `12` |
| `--grid-gutter` | `28px` |
| `--grid-sm-gutter` | `12px` |
| `--header-height` | `60px` |
| `--motion-duration-100` | `100ms` |
| `--motion-duration-150` | `150ms` |
| `--motion-duration-200` | `200ms` |
| `--motion-duration-250` | `250ms` |
| `--motion-duration-300` | `300ms` |
| `--motion-timing-function-ease-in` | `ease-in` |
| `--motion-timing-function-ease-in-out-cubic` | `cubic-bezier(0.645,0.045,0.355,1)` |
| `--motion-timing-function-ease-in-out-linear` | `cubic-bezier(0.5,0,0.5,1)` |
| `--motion-timing-function-ease-in-out-quad` | `cubic-bezier(0.45,0,0.55,1)` |
| `--motion-timing-function-ease-in-out-quart` | `cubic-bezier(0.76,0,0.24,1)` |
| `--motion-timing-function-ease-in-out-quint` | `cubic-bezier(0.86,0,0.07,1)` |
| `--motion-timing-function-ease-out` | `ease-out` |
| `--motion-timing-function-linear` | `linear` |
| `--offset-absolute-0` | `0` |
| `--offset-absolute-1` | `0.0625rem` |
| `--offset-absolute-2` | `0.125rem` |
| `--shadow-100` | `0px 0.7px 1.462px rgba(0,0,0,.015),0px 3px 9px #00000008` |
| `--shadow-200` | `0px 0.175px 1.041px rgba(0,0,0,.013),0px 0.8px 2.925px #00000005,0px 2.025px 7.847px rgba(0,0,0,.027),0px 4px 18px #0000000a` |
| `--shadow-300` | `0px 0.667px 3.502px #00000003,0px 2.933px 7.252px rgba(0,0,0,.016),0px 7.2px 14.462px #00000005,0px 13.867px 28.348px rgba(0,0,0,.024),0px 23.333px 52.123px #00000008,0px 36px 89px #0000000a` |
| `--size-block-header-icon` | `26px` |
| `--spacing-0` | `0` |
| `--spacing-12` | `0.75rem` |
| `--spacing-128` | `8rem` |
| `--spacing-16` | `1rem` |
| `--spacing-160` | `10rem` |
| `--spacing-20` | `1.25rem` |
| `--spacing-24` | `1.5rem` |
| `--spacing-28` | `1.75rem` |
| `--spacing-30` | `1.875rem` |
| `--spacing-32` | `2rem` |
| `--spacing-4` | `0.25rem` |
| `--spacing-40` | `2.5rem` |
| `--spacing-48` | `3rem` |
| `--spacing-56` | `3.5rem` |
| `--spacing-64` | `4rem` |
| `--spacing-72` | `4.5rem` |
| `--spacing-8` | `0.5rem` |
| `--spacing-80` | `5rem` |
| `--spacing-96` | `6rem` |
| `--spacing-block-l` | `32px` |
| `--spacing-block-m` | `24px` |
| `--spacing-block-s` | `20px` |
| `--spacing-l` | `80px` |
| `--spacing-m` | `40px` |
| `--spacing-s` | `40px` |
| `--spacing-xl` | `80px` |
| `--spacing-xs` | `20px` |
| `--text-color-dark` | `#111` |
| `--text-color-extra-light` | `#0003` |
| `--text-color-light` | `#0006` |
| `--text-color-medium` | `#0009` |
| `--text-color-regular` | `#040404` |
| `--thickness-absolute-1` | `0.0625rem` |
| `--thickness-absolute-2` | `0.125rem` |
| `--typography-mono-100-bold-font` | `700 0.875rem /1.25rem "iA Writer Mono",Nitti,Menlo,Courier,monospace` |
| `--typography-mono-100-bold-letter-spacing` | `-0.0078125rem` |
| `--typography-mono-100-regular-font` | `400 0.875rem /1.25rem "iA Writer Mono",Nitti,Menlo,Courier,monospace` |
| `--typography-mono-100-regular-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-100-bold-font` | `700 0.875rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-100-bold-letter-spacing` | `0` |
| `--typography-sans-100-medium-font` | `500 0.875rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-100-medium-letter-spacing` | `0` |
| `--typography-sans-100-regular-font` | `400 0.875rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-100-regular-letter-spacing` | `0` |
| `--typography-sans-100-semibold-font` | `600 0.875rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-100-semibold-letter-spacing` | `0` |
| `--typography-sans-1000-bold-font` | `700 4.75rem /5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-1000-bold-letter-spacing` | `-0.15625rem` |
| `--typography-sans-1000-regular-font` | `400 4.75rem /5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-1000-regular-letter-spacing` | `-0.25rem` |
| `--typography-sans-150-bold-font` | `700 0.9375rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-150-bold-letter-spacing` | `0` |
| `--typography-sans-150-medium-font` | `500 0.9375rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-150-medium-letter-spacing` | `0` |
| `--typography-sans-150-regular-font` | `400 0.9375rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-150-regular-letter-spacing` | `0` |
| `--typography-sans-150-semibold-font` | `600 0.9375rem /1.25rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-150-semibold-letter-spacing` | `0` |
| `--typography-sans-200-bold-font` | `700 1rem /1.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-200-bold-letter-spacing` | `0` |
| `--typography-sans-200-medium-font` | `500 1rem /1.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-200-medium-letter-spacing` | `0` |
| `--typography-sans-200-regular-font` | `400 1rem /1.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-200-regular-letter-spacing` | `0` |
| `--typography-sans-200-semibold-font` | `600 1rem /1.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-200-semibold-letter-spacing` | `0` |
| `--typography-sans-300-bold-font` | `700 1.125rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-300-bold-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-300-medium-font` | `500 1.125rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-300-medium-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-300-regular-font` | `400 1.125rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-300-regular-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-300-semibold-font` | `600 1.125rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-300-semibold-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-350-bold-font` | `700 1.25rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-350-bold-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-350-medium-font` | `500 1.25rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-350-medium-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-350-regular-font` | `400 1.25rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-350-regular-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-350-semibold-font` | `600 1.25rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-350-semibold-letter-spacing` | `-0.0078125rem` |
| `--typography-sans-400-bold-font` | `700 1.375rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-400-bold-letter-spacing` | `-0.015625rem` |
| `--typography-sans-400-medium-font` | `500 1.375rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-400-medium-letter-spacing` | `-0.015625rem` |
| `--typography-sans-400-regular-font` | `400 1.375rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-400-regular-letter-spacing` | `-0.015625rem` |
| `--typography-sans-400-semibold-font` | `600 1.375rem /1.75rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-400-semibold-letter-spacing` | `-0.015625rem` |
| `--typography-sans-50-bold-font` | `700 0.75rem /1rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-50-bold-letter-spacing` | `0.0078125rem` |
| `--typography-sans-50-medium-font` | `500 0.75rem /1rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-50-medium-letter-spacing` | `0.0078125rem` |
| `--typography-sans-50-regular-font` | `400 0.75rem /1rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-50-regular-letter-spacing` | `0.0078125rem` |
| `--typography-sans-50-semibold-font` | `600 0.75rem /1rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-50-semibold-letter-spacing` | `0.0078125rem` |
| `--typography-sans-500-bold-font` | `700 1.625rem /2rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-500-bold-letter-spacing` | `-0.0390625rem` |
| `--typography-sans-500-medium-font` | `500 1.625rem /2rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-500-medium-letter-spacing` | `-0.0390625rem` |
| `--typography-sans-500-semibold-font` | `600 1.625rem /2rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-500-semibold-letter-spacing` | `-0.0390625rem` |
| `--typography-sans-600-bold-font` | `700 2rem /2.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-600-bold-letter-spacing` | `-0.046875rem` |
| `--typography-sans-600-regular-font` | `400 2rem /2.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-600-regular-letter-spacing` | `-0.0625rem` |
| `--typography-sans-600-semibold-font` | `600 2rem /2.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-600-semibold-letter-spacing` | `-0.046875rem` |
| `--typography-sans-700-bold-font` | `700 2.625rem /3rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-700-bold-letter-spacing` | `-0.09375rem` |
| `--typography-sans-700-regular-font` | `400 2.625rem /3rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-700-regular-letter-spacing` | `-0.125rem` |
| `--typography-sans-700-semibold-font` | `600 2.625rem /3rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-700-semibold-letter-spacing` | `-0.09375rem` |
| `--typography-sans-800-bold-font` | `700 3.375rem /3.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-800-bold-letter-spacing` | `-0.1171875rem` |
| `--typography-sans-800-regular-font` | `400 3.375rem /3.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-800-regular-letter-spacing` | `-0.21875rem` |
| `--typography-sans-800-semibold-font` | `600 3.375rem /3.5rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-800-semibold-letter-spacing` | `-0.1171875rem` |
| `--typography-sans-900-bold-font` | `700 4rem /4rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-900-bold-letter-spacing` | `-0.1328125rem` |
| `--typography-sans-900-regular-font` | `400 4rem /4rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-900-regular-letter-spacing` | `-0.171875rem` |
| `--typography-sans-900-semibold-font` | `600 4rem /4rem NotionInter,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol"` |
| `--typography-sans-900-semibold-letter-spacing` | `-0.1328125rem` |
| `--typography-serif-200-regular-font` | `400 1rem /1.5rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-200-regular-letter-spacing` | `0` |
| `--typography-serif-300-regular-font` | `400 1.125rem /1.75rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-300-regular-letter-spacing` | `0` |
| `--typography-serif-350-regular-font` | `400 1.25rem /1.75rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-350-regular-letter-spacing` | `0` |
| `--typography-serif-400-regular-font` | `400 1.375rem /1.75rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-400-regular-letter-spacing` | `0` |
| `--typography-serif-500-regular-font` | `400 1.625rem /2rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-500-regular-letter-spacing` | `0` |
| `--typography-serif-600-regular-font` | `400 2rem /2.5rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-600-regular-letter-spacing` | `0` |
| `--typography-serif-700-regular-font` | `400 2.625rem /3rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-700-regular-letter-spacing` | `-0.09375rem` |
| `--typography-serif-800-regular-font` | `400 3.375rem /3.5rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-800-regular-letter-spacing` | `-0.125rem` |
| `--typography-serif-900-regular-font` | `400 4rem /4rem "Lyon Text",Georgia,YuMincho,"Yu Mincho","Hiragino Mincho ProN","Hiragino Mincho Pro","Songti TC","Songti SC",SimSun,"Nanum Myeongjo",NanumMyeongjo,Batang,serif` |
| `--typography-serif-900-regular-letter-spacing` | `-0.125rem` |
| `--z-index-banner` | `90` |
| `--z-index-header` | `100` |
| `--z-index-lightbox` | `500` |
| `--z-index-mobile-nav` | `200` |
| `--z-index-popup` | `500` |
| `--z-index-tooltip` | `500` |


## Color Palette

### Backgrounds
- `rgb(246, 245, 244)` — near-white
- `rgb(2, 9, 58)` — near-black
- `rgb(69, 93, 211)`
- `rgb(255, 201, 94)` — light
- `rgb(247, 116, 99)`
- `rgb(98, 174, 240)`
- `rgb(173, 109, 237)`
- `rgb(255, 138, 51)`
- `rgb(255, 131, 221)`
- `rgb(33, 49, 131)` — dark
- `rgba(0, 0, 0, 0.05)` — near-black
- `rgba(255, 255, 255, 0)` — near-white
- `rgb(255, 255, 255)` — near-white
- `rgb(0, 0, 0)` — near-black
- `rgb(42, 157, 153)`

### Text Colors
- `rgba(0, 0, 0, 0.95)` — near-black
- `rgba(0, 0, 0, 0.9)` — near-black
- `rgb(9, 127, 232)`
- `rgb(0, 117, 222)`
- `rgb(246, 245, 244)` — near-white
- `rgb(255, 255, 255)` — near-white
- `rgb(98, 174, 240)`
- `rgba(255, 255, 255, 0.75)` — near-white
- `rgb(0, 0, 0)` — near-black
- `rgba(0, 0, 0, 0.59)` — near-black
- `rgba(0, 0, 0, 0.54)` — near-black
- `rgb(97, 93, 89)` — neutral gray
- `rgb(163, 158, 152)` — light gray
- `rgb(25, 25, 24)` — dark

### Border Colors
- `rgba(255, 255, 255, 0)`
- `rgba(255, 255, 255, 0.1)`
- `rgba(0, 0, 0, 0.1)`
- `rgb(221, 221, 221)`
- `rgba(0, 0, 0, 0.9) rgb(247, 247, 245) rgb(247, 247, 245) rgba(0, 0, 0, 0.9)`

**Likely accent color**: `rgb(0, 117, 222)`


## Typography

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Display / H1 | NotionInter | 64px | 700 | 64px | -2.125px |
| Display / H1 | NotionInter | 54px | 700 | 56px | -1.875px |
| Display / H1 | NotionInter | 48px | 400 | 0px | normal |
| Display / H1 | NotionInter | 42px | 700 | 48px | -1.5px |
| Display / H1 | NotionInter | 40px | 400 | 60px | normal |
| Display / H1 | Lyon Text | 32px | 400 | 40px | normal |
| H2 | NotionInter | 26px | 700 | 32px | -0.625px |
| H3 | NotionInter | 24px | 500 | 20px | normal |
| H2 | NotionInter | 22px | 700 | 28px | -0.25px |
| Body | NotionInter | 22px | 400 | 33px | normal |
| H3 | NotionInter | 20px | 600 | 28px | -0.125px |
| Body | NotionInter | 20px | 400 | 30px | normal |
| Body | NotionInter | 16px | 400 | 24px | normal |
| Body | NotionInter | 16px | 500 | 24px | normal |
| Body | NotionInter | 16px | 700 | 24px | normal |
| Body | NotionInter | 16px | 600 | 24px | normal |
| Body | NotionInter | 15px | 400 | 20px | normal |
| Body small | NotionInter | 14px | 400 | 20px | normal |
| Body small | NotionInter | 14px | 500 | 20px | normal |
| Body small | NotionInter | 14px | 600 | 20px | normal |
| Caption / Small | NotionInter | 12px | 400 | 16px | 0.125px |
| Caption / Small | NotionInter | 12px | 500 | 16px | 0.125px |
| Body | NotionInter | 0px | 400 | 0px | normal |

**Font families in use**: Lyon Text, NotionInter


## Spacing Scale

`2px` · `3px` · `3.2px` · `4px` · `4.66832px` · `5px` · `6px` · `7px` · `8px` · `9.39062px` · `10px` · `12px` · `14px` · `15px` · `16px` · `20px` · `24px` · `28px` · `32px` · `34px`


## Borders, Radii & Effects

**Border radius values**: `50%`, `100%`, `4px`, `5px`, `8px`, `12px 12px 0px 0px`, `12px`, `12px 0px 0px`, `9999px`

**Border widths**: `0px 1px 1px 0px`, `1px`

**Box shadows**:
- `rgba(0, 0, 0, 0.1) 0px 1px 0px 0px`
- `rgba(255, 255, 255, 0.2) 0px 0px 20px 5px`
- `rgba(0, 0, 0, 0.01) 0px 0.175px 1.041px 0px, rgba(0, 0, 0, 0.02) 0px 0.8px 2.925px 0px, rgba(0, 0, 0, 0.027) 0px 2.025px 7.847px 0px, rgba(0, 0, 0, 0.04) 0px 4px 18px 0px`
- `rgba(0, 0, 0, 0.01) 0px 1px 3px 0px, rgba(0, 0, 0, 0.02) 0px 3px 7px 0px, rgba(0, 0, 0, 0.02) 0px 7px 15px 0px, rgba(0, 0, 0, 0.04) 0px 14px 28px 0px, rgba(0, 0, 0, 0.05) 0px 23px 52px 0px`
- `rgba(0, 0, 0, 0.01) 0px 0.667px 3.502px 0px, rgba(0, 0, 0, 0.016) 0px 2.933px 7.252px 0px, rgba(0, 0, 0, 0.02) 0px 7.2px 14.462px 0px, rgba(0, 0, 0, 0.024) 0px 13.867px 28.348px 0px, rgba(0, 0, 0, 0.03) 0px 23.333px 52.123px 0px, rgba(0, 0, 0, 0.04) 0px 36px 89px 0px`

**Visual effects**:
- `filter: url("#hph-illustration-filter-desktop")`
- `backdrop-filter: blur(12px)`
- `filter: drop-shadow(rgba(0, 0, 0, 0.1) 0px 4px 12px)`


## Component Patterns

### Buttons

- **"Change to English (UK)→"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(0, 117, 222)`
  - Font: 14px 400
  - Padding: `0px`
  - Border radius: `0px`
  - Border: `0px none rgb(0, 117, 222)`

- **""**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgba(0, 0, 0, 0.95)`
  - Font: 16px 400
  - Padding: `0px`
  - Border radius: `0px`
  - Border: `0px none rgba(0, 0, 0, 0.95)`

- **"Product"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(246, 245, 244)`
  - Font: 16px 400
  - Padding: `5px 10px`
  - Border radius: `4px`
  - Border: `0px none rgb(246, 245, 244)`

- **"Get Notion free"**
  - Background: `rgb(69, 93, 211)`
  - Color: `rgb(255, 255, 255)`
  - Font: 16px 500
  - Padding: `4px 14px`
  - Border radius: `8px`
  - Border: `1px solid rgba(255, 255, 255, 0)`

### Form Inputs

- **checkbox** input
  - Background: `rgba(0, 0, 0, 0)`
  - Font size: `16px`
  - Padding: `0px`
  - Border radius: `0px`

### Navigation

- **Nav** with 47 links: , NotionYour AI workspace, Notion Calendar, Notion Mail, Notion AIAI tools for work, AgentsAutomate busywork
  - Layout: `grid`, gap: `normal`

- **Nav** with 50 links: , , , , , 
  - Layout: `flex`, gap: `24px`


## Layout Patterns

### CSS Grid Usage

- `<span>`: columns `16px`, gap `normal`
- `<nav>`: columns `1280px`, gap `normal`
- `<div>`: columns `270.219px 659.562px 270.219px`, gap `16px`
- `<div>`: columns `67.2031px 960px 67.2031px`, gap `40px normal`
- `<span>`: columns `50px`, gap `normal`

### Flexbox Usage

- `<div>`: row, justify: center, align: baseline, gap: 12px (3 children)
- `<div>`: row, align: center, gap: 16px (3 children)
- `<div>`: column (3 children)
- `<header>`: column, justify: start, align: stretch, gap: 28px (3 children)
- `<section>`: column, gap: 32px (2 children)


## Assets Detected

46 images and 26 inline SVG icons detected.

### Images

| Source | Alt | Dimensions |
|--------|-----|------------|
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fshared%2Fnavigation%...` |  | 192px × 161px |
| `https://www.notion.com/front-static/agents/tasks/check.svg` |  | 48px × 48px |
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fbook.png&w=...` |  | 59px × 59px |
| `https://www.notion.com/front-static/agents/tasks/gmail.svg` |  | 49px × 49px |
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fglobe.png&w...` |  | 59px × 59px |
| `https://www.notion.com/front-static/agents/tasks/hubspot.svg` |  | 40px × 40px |
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Ffiles-v2.pn...` |  | 51px × 51px |
| `https://www.notion.com/front-static/agents/tasks/github.svg` |  | 43px × 43px |
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fcheckmark.p...` |  | 48px × 48px |
| `https://www.notion.com/front-static/agents/tasks/slack.svg` |  | 42px × 42px |
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Flight_bulb....` |  | 59px × 59px |
| `https://www.notion.com/front-static/agents/tasks/chart.svg` |  | 45px × 45px |
| `https://www.notion.com/_next/image?url=%2Ffront-static%2Fagents%2Fapple.png&w...` |  | 59px × 59px |
| `https://images.ctfassets.net/spoqsaf9291f/4MHGeZRO6fDOLPVyJsLoyQ/73cf5bcef2ed...` | OpenAI | 66px × 24px |
| `https://images.ctfassets.net/spoqsaf9291f/5JgmuggsW4KO8pYqbKUUeW/9d4781445ff3...` | Figma | 56px × 24px |
| `https://images.ctfassets.net/spoqsaf9291f/1DEacqNIZ316cGgB4hhZRL/d77ff0228469...` | Ramp | 71px × 23px |
| `https://images.ctfassets.net/spoqsaf9291f/OJRQbA3XzRNfCfMh3UWf4/76408a06d9d9a...` | Cursor | 74px × 22px |
| `https://images.ctfassets.net/spoqsaf9291f/4Q8UO6GLVXAipkW53CHm33/8ccdeeb5bf18...` | Vercel | 73px × 22px |
| `https://images.ctfassets.net/spoqsaf9291f/1Y4mbag3O14GsqnVtxgyZn/93c685d16fde...` | Nvidia | 79px × 20px |
| `https://images.ctfassets.net/spoqsaf9291f/7ciuOUOhooC7cNnVsY107S/094eda50eab2...` | Volvo | 79px × 20px |

### SVG Icons (26 found)

- (icon) — 16px × 16px
- (icon) — 33px × 34px
- (icon) — 10px × 10px
- (icon) — 48px × 48px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px
- (icon) — 22px × 22px

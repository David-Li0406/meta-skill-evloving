# UdonでのuGUI

## イベント

Button, Slider, Toggleなど、クリックや変化のイベントを取得できますが、UdonSharpでは直接コールバックを指定できず、`SendCustomEvent`を使って通知しています。この関係で、SliderやToggleの引数は取得できません。

したがって以下のように、変更を検知したら、インスペクタにセットされたスライダー情報を読み取る形にします。

```cs
// Sliderの参照
public Slider slider;

// この関数をSliderのOn Value Changedに登録
public void OnSliderChange()
{
    var value = slider.value;
}
```
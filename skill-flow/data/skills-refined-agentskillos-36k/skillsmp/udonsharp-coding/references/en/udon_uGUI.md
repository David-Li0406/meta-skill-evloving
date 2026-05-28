# uGUI in Udon

## Events

You can receive click/change events from UI components such as Button, Slider, and Toggle. However, in UdonSharp you cannot assign callbacks directly, so notifications are typically sent using `SendCustomEvent`. Because of this, you cannot receive the Slider/Toggle value as an event argument.

Therefore, detect the change and then read the UI component’s current value via the reference set in the Inspector.

```cs
// Reference to the Slider
public Slider slider;

// Register this function to the Slider's On Value Changed
public void OnSliderChange()
{
    var value = slider.value;
}
```

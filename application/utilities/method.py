



def map_triger(trigger, slider, value):
    if 'value' in trigger:
        slider = value
    elif 'slider' in trigger:
        value = slider
    return slider, value


from .version import __version__


def main():
    import argparse
    from .pironman5 import Pironman5
    from pm_auto.ws2812 import RGB_STYLES
    from pm_auto.fan_control import GPIO_FAN_MODES
    import sys

    AUTO_CONFIG_KEYS = [
        'rgb_color',
        'rgb_brightness',
        'rgb_style',
        'rgb_speed',
        'rgb_enable',
        'rgb_led_count',
        'temperature_unit',
        'gpio_fan_mode',
        'gpio_fan_pin',
    ]

    parser = argparse.ArgumentParser(description='Pironman5')
    parser.add_argument("command",
                        choices=["start", "stop"],
                        nargs="?",
                        help="Command")
    parser.add_argument("--config", action="store_true", help="Show config")
    parser.add_argument("--rgb-color", help="RGB color")
    parser.add_argument("--rgb-brightness", type=int, help="RGB brightness")
    parser.add_argument("--rgb-style", choices=RGB_STYLES, help="RGB style")
    parser.add_argument("--rgb-speed", type=int, help="RGB speed")
    parser.add_argument("--rgb-enable", type=bool, help="RGB enable")
    parser.add_argument("--rgb-led-count", type=int, help="RGB LED count")
    parser.add_argument("--temperature-unit",
                        choices=["C", "F"],
                        help="Temperature unit")
    parser.add_argument("--gpio-fan-mode", type=int, help=f"GPIO fan mode, 0-4, {GPIO_FAN_MODES}")
    parser.add_argument("--gpio-fan-pin", type=int, help="GPIO fan pin")

    args = parser.parse_args()
    args = vars(args)

    if not (len(sys.argv) > 1):
        parser.print_help()
        quit()

    auto_config = {}
    for key in AUTO_CONFIG_KEYS:
        if args[key] is not None:
            auto_config[key] = args[key]
    config = {
        'auto': auto_config,
    }

    if args['config']:
        from pkg_resources import resource_filename
        import json
        CONFIG_PATH = resource_filename('pironman5', 'config.json')
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        print(json.dumps(config, indent=4))
        quit()

    if args['command'] == "stop":
        import os
        os.system('kill -9 $(pgrep -f "pironman5 start")')
        os.system('kill -9 $(pgrep -f "pironman5-service start")')
        pironman5 = Pironman5()
        pironman5.stop()

    Pironman5.update_config_file(config)
    if args['command'] == "start":
        pironman5 = Pironman5()
        pironman5.start()
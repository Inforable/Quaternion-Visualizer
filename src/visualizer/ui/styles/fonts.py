class UIFonts:
    # Jenis font
    FAMILY = "Arial"
    MONOSPACE_FAMILY = "Courier"

    # Ukuran font
    TITLE_SIZE = 12
    LARGE_SIZE = 14
    NORMAL_SIZE = 10
    SMALL_SIZE = 8

    # Font weight
    NORMAL_WEIGHT = "normal"
    BOLD_WEIGHT = "bold"

    @staticmethod
    def get_title_font() -> dict:
        return {
            "family": UIFonts.FAMILY,
            "size": UIFonts.TITLE_SIZE,
            "weight": UIFonts.BOLD_WEIGHT
        }
    
    @staticmethod
    def get_normal_font() -> dict:
        return {
            "family": UIFonts.FAMILY,
            "size": UIFonts.NORMAL_SIZE,
            "weight": UIFonts.NORMAL_WEIGHT
        }
    
    @staticmethod
    def get_small_font() -> dict:
        return {
            "family": UIFonts.FAMILY,
            "size": UIFonts.SMALL_SIZE,
            "weight": UIFonts.NORMAL_WEIGHT
        }
    
    @staticmethod
    def get_monospace_font() -> dict:
        return {
            "family": UIFonts.MONOSPACE_FAMILY,
            "size": UIFonts.NORMAL_SIZE,
            "weight": UIFonts.NORMAL_WEIGHT
        }
    
    @staticmethod
    def get_font_stylesheet(font_config) -> str:
        return f"font-family: {font_config['family']}; font-size: {font_config['size']}px; font-weight: {font_config['weight']};"
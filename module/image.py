import io
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from models import database
from module.statsType import StatsPlayType
from utils.directory import directory
from utils.location import comment


class ImageProcess:
    def __init__(self, player_info: database.Player, language: str):
        self.background_canvas = Image.open(
            fp=os.path.join(directory, "assets", "background", "background_1.png")
        )
        self.player_name_font = ImageFont.truetype(
            os.path.join(directory, "assets", "fonts", "NotoSansKR-Black.otf"),
            size=36
        )
        self.sub_title_font = ImageFont.truetype(
            os.path.join(directory, "assets", "fonts", "TmoneyRoundWindExtraBold.otf"),
            size=16
        )
        self.sub_description_font = ImageFont.truetype(
            os.path.join(directory, "assets", "fonts", "TmoneyRoundWindExtraBold.otf"),
            size=20
        )
        self.player = player_info
        self.language = language

    def normal_stats(self, stats: dict[StatsPlayType, database.NormalStats | None]):
        canvas = Image.new('RGBA', (768, 433))
        layout_canvas = Image.open(
            fp=os.path.join(directory, "assets", "layout", "normal_layout.png")
        )

        canvas.paste(self.background_canvas, (0, 0))
        canvas.paste(layout_canvas, (0, 0))

        draw_canvas = ImageDraw.Draw(canvas)

        # Player Title
        _, player_name_text_h = draw_canvas.textsize(self.player.name, font=self.player_name_font)
        draw_canvas.text(
            (22, (80 - player_name_text_h) / 2),
            self.player.name,
            font=self.player_name_font,
            fill="#f1ca09"
        )

        # Solo / Duo / Squad
        for category_position, game_type in enumerate([
            StatsPlayType.SOLO,
            StatsPlayType.DUO,
            StatsPlayType.SQUAD
        ]):
            game_data = stats.get(game_type)

            draw_canvas.rectangle(
                (
                    30 + (((canvas.width - 80) / 3) + 30) * category_position,
                    158,
                    (30 + (canvas.width - 80) / 3) * (category_position + 1) + category_position * 10,
                    178
                ), fill="#af2222"
            )
            deployment = [
                {
                    "kda": round((game_data.kills + game_data.assists) / game_data.deaths, 2),
                    "win_ratio": round(game_data.wins / game_data.played * 100, 1)
                }, {
                    "average_deals": round(game_data.deals / game_data.played, 1),
                    "max_kills": game_data.kills
                }
            ]
            # KDA / Win ratio / Average Deals / Max Kill
            for sub_title_position, item in enumerate(deployment):
                height = [230, 291]
                for index, (key, value) in enumerate(item.items()):
                    sub_title1_w, sub_title1_h = draw_canvas.textsize("KDA", font=self.sub_title_font)
                    draw_canvas.text(
                        (
                            20 * (category_position + 1)
                            + (canvas.width - 80) / 12 * (1 + 2 * (category_position * 2 + sub_title_position))
                            - sub_title1_w / 2,
                            230 + height[index] * 61
                        ),
                        text=comment('normal_stats', key, self.language),
                        fill="#f1ca09",
                        font=self.sub_title_font
                    )
                    sub_description1_w, sub_description1_h = draw_canvas.textsize("5.08", font=self.sub_title_font)
                    draw_canvas.text(
                        (
                            20 * (category_position + 1)
                            + (canvas.width - 80) / 12 * (1 + 2 * (category_position * 2 + sub_title_position))
                            - sub_description1_w / 2,
                            260 + height[index] * 61
                        ),
                        text=value,
                        fill="#ffffff",
                        font=self.sub_title_font
                    )

        # draw_canvas.
        canvas.show()
        return

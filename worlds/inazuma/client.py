# --- inazuma_client.py ---
import logging
from .Items import ItemData, ItemClassification

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient


# --- Configuración de capítulos ---
inazuma_chapters = {
    "Prologue": ItemData(20050008, ItemClassification.progression),
    "Chapter1": ItemData(20050009, ItemClassification.progression),
    "Chapter2": ItemData(20050010, ItemClassification.progression)
}

# --- Configuración de victorias contra equipos ---
victory_locations = {
    0x23: ItemData(100001, ItemClassification.progression),  # Secret Service Team
}

class InazumaClient(BizHawkClient):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("InazumaClient")
        self.reported_chapters = set()
        self.reported_victories = set()

    async def check_chapters(self):
        """
        Lee los offsets de RAM de capítulos y reporta avance en la historia.
        """
        # Ejemplo: offsets conocidos para cada capítulo
        chapter_offset_map = {
            0x0CA25A: "id_chapter",
            0x0DDC8E: "flag_chapter",
            0x0D3AC8: "chapter_dword"
        }

        for offset, chapter_name in chapter_offset_map.items():
            value = self.read_byte(offset)  # Ajusta si es byte, word o dword
            chapter_item = inazuma_chapters.get(chapter_name)
            if chapter_item and chapter_name not in self.reported_chapters:
                await self.send_msgs([
                    {"cmd": "LocationChecks", "locations": [chapter_item.id]}
                ])
                self.logger.info(f"Capítulo {chapter_name} completado y reportado!")
                self.reported_chapters.add(chapter_name)

    async def check_victories(self):
        """
        Revisa los offsets de RAM para reportar victorias contra equipos.
        """
        enemy_id = self.read_byte(0x0C9DE4)
        local_score = self.read_byte(0x0C9DE8)
        visitor_score = self.read_byte(0x0C9DE9)

        if local_score > visitor_score and enemy_id not in self.reported_victories:
            location_data = victory_locations.get(enemy_id)
            if location_data:
                await self.send_msgs([
                    {"cmd": "LocationChecks", "locations": [location_data.id]}
                ])
                self.logger.info(f"Victoria contra equipo ID 0x{enemy_id:02X} reportada!")
                self.reported_victories.add(enemy_id)

    async def poll_game_state(self):
        """
        Loop principal que chequea el progreso y victorias periódicamente.
        """
        while True:
            await self.check_chapters()
            await self.check_victories()
            await self.wait(0.5)  # medio segundo de pausa entre chequeos

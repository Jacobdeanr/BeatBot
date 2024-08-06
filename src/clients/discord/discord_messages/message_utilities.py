import discord.embeds
class EmbedUtilities:
    @staticmethod
    def convertMillis(millis):
        seconds = int(millis / 1000) % 60
        minutes = int(millis / (1000 * 60)) % 60
        hours = int(millis / (1000 * 60 * 60)) % 24
        return seconds, minutes, hours
    
    @staticmethod
    def create_embed(title, description="", color=0xb526d9, url=None, image_url=None, fields=None):
        embed = discord.Embed(title=title, description=description, color=color, url=url)
        if image_url:
            embed.set_image(url=image_url)
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        return embed
    
    @staticmethod
    def get_popularity_name(score) -> str:
        if 0 <= score <= 2:
            return "Ghost Town"
        elif 3 <= score <= 5:
            return "Hidden Gem"
        elif 6 <= score <= 10:
            return "Under the Radar"
        elif 11 <= score <= 15:
            return "Whisper in the Wind"
        elif 16 <= score <= 20:
            return "Buzz Builder"
        elif 21 <= score <= 30:
            return "On the Up and Up"
        elif 31 <= score <= 35:
            return "Crowd Pleaser"
        elif 36 <= score <= 40:
            return "Talk of the Town"
        elif 41 <= score <= 50:
            return "Trendsetter"
        elif 51 <= score <= 55:
            return "Hot Topic"
        elif 56 <= score <= 60:
            return "People’s Choice"
        elif 61 <= score <= 70:
            return "Chart Climber"
        elif 71 <= score <= 75:
            return "Viral Sensation"
        elif 76 <= score <= 80:
            return "Cultural Phenomenon"
        elif 81 <= score <= 85:
            return "Icon in the Making"
        elif 86 <= score <= 90:
            return "Hall of Fame"
        elif 91 <= score <= 95:
            return "Mythic Status"
        elif 96 <= score <= 100:
            return "Universal Acclaim"
        else:
            return str(score)
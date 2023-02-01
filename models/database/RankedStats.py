import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

from module.pubgpy import RankedStats as pubgRankedStats

base = declarative_base()


class RankedStats(base):
    __tablename__ = "ranked_stats"

    account_id_with_session = Column(String, primary_key=True)
    account_id = Column(String)
    season = Column(String)
    update_time = Column(DateTime)
    current_tier = Column(String)
    current_sub_tier = Column(String)
    current_point = Column(String)
    best_tier = Column(String)
    best_sub_tier = Column(String)
    best_point = Column(String)

    average_rank = Column(Float, default=0.0)
    deals = Column(Float, default=0.0)
    deaths = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    top10s = Column(Integer, default=0)
    kda_point = Column(Float, default=0.0)
    played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    win_point = Column(Float, default=0.0)

    @classmethod
    def from_pubg(
            cls,
            player: str,
            season: str,
            stats: pubgRankedStats,
            update_time: datetime.datetime = datetime.datetime.now()
    ):
        account_id_with_session = "{}_{}".format(player, season)
        return cls(
            account_id_with_session=account_id_with_session,
            account_id=player,
            season=season,
            update_time=update_time,
            current_tier=stats.current.tier,
            current_sub_tier=stats.current.subtier,
            current_point=stats.current.point,
            best_tier=stats.best.tier,
            best_sub_tier=stats.best.subtier,
            best_point=stats.best.point,
            average_rank=stats.avg_rank,
            deals=stats.damage_dealt,
            deaths=stats.deaths,
            kills=stats.kills,
            assists=stats.assists,
            top10s=stats.top10s,
            kda_point=stats.kda,
            played=stats.rounds_played,
            wins=stats.wins,
            win_point=stats.win_ratio
        )

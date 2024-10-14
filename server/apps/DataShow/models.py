from django.db import models

from utils.models import BaseModel


class Stock(BaseModel):
    id = models.CharField(max_length=64, primary_key=True, verbose_name="股票id")
    open = models.FloatField(verbose_name="开盘价")
    high = models.FloatField(verbose_name="最高价")
    low = models.FloatField(verbose_name="最低价")
    close = models.FloatField(verbose_name="收盘价")
    volume = models.BigIntegerField(verbose_name="交易额")

    class Meta:
        db_table = "tb_stock"
        verbose_name = '股票信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

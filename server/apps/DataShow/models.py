from django.db import models
from django.utils import timezone

from utils.models import BaseModel


class Stock(BaseModel):
    股票名称 = models.CharField(max_length=255, null=True, verbose_name="股票名称")
    股票代码 = models.CharField(max_length=10, null=True, verbose_name="股票代码")
    日期 = models.DateField(verbose_name="日期")
    开盘价 = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="开盘价")
    收盘价 = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="收盘价")
    最高价 = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="最高价")
    最低价 = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="最低价")
    成交量 = models.BigIntegerField(null=True, verbose_name="成交量")
    成交额 = models.DecimalField(max_digits=20, decimal_places=2, null=True, verbose_name="成交额")
    振幅 = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="振幅")  # 通常以百分比表示
    涨跌幅 = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="涨跌幅")  # 百分比
    涨跌额 = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="涨跌额")
    换手率 = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="换手率")  # 百分比

    class Meta:
        db_table = "tb_stock"
        verbose_name = '股票信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

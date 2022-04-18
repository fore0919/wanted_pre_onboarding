from django.db import models

from core.models import TimeStamp

class Product(TimeStamp):
    title = models.CharField(max_length=40) # 펀딩 상품 제목
    user = models.ForeignKey('users.User', on_delete=models.PROTECT) # 게시자명
    description = models.TextField() # 상품 설명
    total_target_amount = models.DecimalField(max_digits=10, decimal_places=2) # 목표금액
    end_date = models.DateField() # 펀딩 종료일
    funding_amount = models.DecimalField(max_digits=10, decimal_places=2) # 1회 펀딩금액 

    class Meta:
        db_table = 'products'


class Detail(models.Model):
    product_id = models.OneToOneField('Product', on_delete=models.CASCADE)
    total_sponsor = models.IntegerField() # 펀딩 참여자 수
    current_funding_amount = models.DecimalField(max_digits=10, decimal_places=2) # 현재 모금 금액 
    target_rate = models.DecimalField(max_digits=5, decimal_places=0) # 목표금액 달성률

    class Meta:
        db_table = 'details'


class Funding(TimeStamp):
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'fundings'
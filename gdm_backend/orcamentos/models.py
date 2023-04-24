from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    largura = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    altura = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)

class Orcamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    validade = models.DateField()
    itens = models.ManyToManyField(Item)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cliente_aceitou = models.BooleanField(default=False, null=True)
    pago = models.BooleanField(default=False, null=True)
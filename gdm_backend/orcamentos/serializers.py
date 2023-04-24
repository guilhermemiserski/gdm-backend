from rest_framework import serializers
from .models import Item, Cliente, Orcamento

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class OrcamentoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    itens = ItemSerializer(many=True)

    class Meta:
        model = Orcamento
        fields = '__all__'

    def update(self, instance, validated_data):
        cliente_data = validated_data.pop('cliente', None)
        itens_data = validated_data.pop('itens', None)

        # Atualiza o cliente (se houver dados)
        if cliente_data:
            cliente_serializer = ClienteSerializer(instance.cliente, data=cliente_data)
            if cliente_serializer.is_valid():
                cliente_serializer.save()
            instance.cliente = cliente_serializer.instance

        # Atualiza os itens (se houver dados)
        if itens_data:
            instance.itens.clear()
            for item_data in itens_data:
                item_id = item_data.get('id')
                if item_id:
                    item = Item.objects.get(pk=item_id)
                    item_serializer = ItemSerializer(item, data=item_data)
                else:
                    item_serializer = ItemSerializer(data=item_data)
                if item_serializer.is_valid():
                    item = item_serializer.save()
                    instance.itens.add(item)

        # Atualiza o restante dos campos
        instance = super().update(instance, validated_data)

        return instance


    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente', None)
        if cliente_data is not None:
            cliente, _ = Cliente.objects.update_or_create(defaults=cliente_data, **cliente_data)
        else:
            cliente = None

        itens_data = validated_data.pop('itens', [])
        orcamento = Orcamento.objects.create(cliente=cliente, **validated_data)

        total = 0
        for item_data in itens_data:
            item = Item.objects.create(**item_data)
            orcamento.itens.add(item)
            total += item.valor * item.quantidade

        orcamento.total = total
        orcamento.save()

        return orcamento
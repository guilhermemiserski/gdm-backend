from rest_framework import viewsets, status
from .models import Item, Cliente, Orcamento
from .serializers import ItemSerializer, ClienteSerializer, OrcamentoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Cliente.objects.filter(cpf=serializer.validated_data['cpf']).exists():
            return Response({'cpf': ['Já existe um cliente com este CPF.']}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    
    @action(detail=False, methods=['get'])
    def buscar_orcamentos_aceitos_pelo_cliente(self, request):
        queryset = self.get_queryset().filter(cliente_aceitou=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
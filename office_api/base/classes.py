from rest_framework import mixins


class CreateUpdateDestroyListRetrieve(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                                      mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pass

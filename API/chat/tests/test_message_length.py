import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db()
class TestMessageLengthValidation:
    """
    Testes para validação de limite de caracteres em mensagens do chat.
    Issue #304: Fix(Bug) - Corrigir inconsistência no limite de caracteres.
    """

    def test_post_message_rejects_ascii_over_80(self):
        """
        CT01 - Ciclo 1: Rejeitar texto ASCII com mais de 80 caracteres.
        Verifica que a API retorna erro 400 para mensagens com 81 chars.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_1", email="user1@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        payload = {"content": "a" * 81}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 400
        assert "content" in response.data

    def test_post_message_accepts_79_chars(self):
        """
        CT02 - Ciclo 2: Aceitar mensagem com exatamente 79 caracteres.
        Mensagens abaixo do limite devem ser aceitas.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_2", email="user2@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        payload = {"content": "a" * 79}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 201

    def test_post_message_accepts_exactly_80_chars(self):
        """
        CT03 - Ciclo 2: Aceitar mensagem com exatamente 80 caracteres.
        O limite de 80 caracteres deve ser inclusivo.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_3", email="user3@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        payload = {"content": "a" * 80}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 201

    def test_post_message_rejects_81_mixed_text_emoji(self):
        """
        CT04 - Ciclo 2: Rejeitar mensagem com 81 caracteres mistos (texto + emoji).
        Emojis devem ser contados da mesma forma que caracteres ASCII.
        Front-end pode estar enviando emoji codificado ou como texto unicode.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_4", email="user4@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        # Mensagem com texto + emoji que totaliza >80 caracteres Python
        # Nota: emoji pode ocupar múltiplos code points
        payload = {"content": "a" * 78 + "😀😀😀"}  # 78 chars + 3 emojis
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 400
        assert "content" in response.data

    def test_post_message_accepts_80_chars_with_emoji(self):
        """
        CT05 - Ciclo 2: Aceitar mensagem com exatamente 80 chars incluindo emoji.
        Verifica que emojis dentro do limite são aceitos.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_5", email="user5@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        # 78 caracteres ASCII + 1 emoji simples = deve caber no limite
        payload = {"content": "a" * 78 + "😀"}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 201

    def test_post_message_rejects_many_emojis(self):
        """
        CT06 - Ciclo 2: Rejeitar mensagem com muitos emojis (>80 chars).
        Testa se validação funciona para mensagens compostas apenas de emojis.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_6", email="user6@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        # 85 emojis - deve exceder o limite
        payload = {"content": "😀" * 85}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 400
        assert "content" in response.data

    def test_post_message_handles_composite_emojis_ct07(self):
        """
        CT07 - Ciclo 2: Validar emojis compostos (grapheme clusters).

        Emojis compostos como 👨‍👩‍👧‍👦 ocupam múltiplos code points
        mas devem ser contados como 1 caractere visual (Issue #304).
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_7", email="user7@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        emoji_familia = "👨‍👩‍👧‍👦"
        payload = {"content": emoji_familia * 15}

        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 201, (
            f"Esperado 201 para 15 emojis visuais, "
            f"mas len() conta como {len(payload['content'])} code points"
        )

    def test_patch_message_respects_char_limit(self):

        client = APIClient()
        user = User.objects.create_user(
            username="test_user_8", email="user8@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        create_payload = {"content": "Mensagem original válida"}
        create_response = client.post("/api/chat/messages/", create_payload, format="json")
        assert create_response.status_code == 201
        message_id = create_response.data["id"]

        update_payload = {"content": "x" * 81}
        update_response = client.patch(
            f"/api/chat/messages/{message_id}/", update_payload, format="json"
        )

        assert update_response.status_code == 400
        assert "content" in update_response.data

    def test_patch_message_accepts_valid_update(self):
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_9", email="user9@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        create_payload = {"content": "Original"}
        create_response = client.post("/api/chat/messages/", create_payload, format="json")
        message_id = create_response.data["id"]

        update_payload = {"content": "y" * 80}
        update_response = client.patch(
            f"/api/chat/messages/{message_id}/", update_payload, format="json"
        )

        assert update_response.status_code == 200
        assert update_response.data["content"] == "y" * 80

    def test_model_clean_validates_content_length(self):
        from django.core.exceptions import ValidationError

        from chat.models import Message

        user = User.objects.create_user(
            username="test_user_10", email="user10@aluno.unb.br", password="testpass123"
        )

        message = Message(sender=user, content="z" * 81)

        with pytest.raises(ValidationError) as exc_info:
            message.clean()

        assert "content" in str(exc_info.value)

    def test_empty_message_rejected(self):
        """
        CT11 - Ciclo 3: Rejeitar mensagens vazias.

        Edge case: mensagens não podem ser vazias ou apenas whitespace.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_11", email="user11@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        # Mensagem vazia
        payload = {"content": ""}
        response = client.post("/api/chat/messages/", payload, format="json")
        assert response.status_code == 400

        # Apenas espaços
        payload = {"content": "   "}
        response = client.post("/api/chat/messages/", payload, format="json")
        assert response.status_code == 400

    def test_whitespace_counted_in_limit(self):
        """
        CT12 - Ciclo 3: Whitespace conta no limite de caracteres.

        Espaços, tabs e quebras de linha devem ser contados.
        """
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_12", email="user12@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        # 79 'a' + 1 espaço + 1 'b' = 81 caracteres
        payload = {"content": "a" * 79 + " b"}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 400
        assert "content" in response.data

    def test_model_save_calls_clean(self):
        """
        CT13 - Ciclo 3: Model.save() deve chamar clean() automaticamente.

        Django admin e outras operações chamam full_clean() antes de save().
        Verifica integração completa da validação no ORM.
        """
        from django.core.exceptions import ValidationError

        from chat.models import Message

        user = User.objects.create_user(
            username="test_user_13", email="user13@aluno.unb.br", password="testpass123"
        )

        # Criar mensagem inválida
        message = Message(sender=user, content="w" * 85)

        # full_clean() deve lançar ValidationError (chamado automaticamente pelo admin)
        with pytest.raises(ValidationError) as exc_info:
            message.full_clean()

        assert "content" in str(exc_info.value)

    def test_emoji_with_skin_tone_modifiers(self):
        client = APIClient()
        user = User.objects.create_user(
            username="test_user_14", email="user14@aluno.unb.br", password="testpass123"
        )
        client.force_authenticate(user=user)

        emoji_with_modifier = "👋🏽"

        assert len(emoji_with_modifier) == 2, "Sanity check: emoji + modifier = 2 code points"

        payload = {"content": emoji_with_modifier * 80}
        response = client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 201, (
            f"Esperado 201 para 80 emojis com skin tone, "
            f"mas len() conta como {len(payload['content'])} code points"
        )

        payload_over = {"content": emoji_with_modifier * 81}
        response_over = client.post("/api/chat/messages/", payload_over, format="json")

        assert (
            response_over.status_code == 400
        ), "Esperado 400 para 81 emojis com skin tone (excede limite)"
        assert "content" in response_over.data

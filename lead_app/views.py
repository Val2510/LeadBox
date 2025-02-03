from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

WORDPRESS_API_URL = "https://caesarboxing.ru/wp-admin/admin-ajax.php?action=handle_wheel_lead"

@csrf_exempt
def receive_wheel_lead(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
            print("📩 Получен лид:", data)

            if not data.get("name") or not data.get("phone"):
                return JsonResponse({"success": False, "error": "Имя и телефон обязательны!"}, status=400)

            wordpress_data = {
                "name": data.get("name"),
                "phone": data.get("phone"),
                "prize": data.get("prize", ""),
                "utm_source": data.get("utm_source", ""),
                "utm_medium": data.get("utm_medium", ""),
                "utm_campaign": data.get("utm_campaign", ""),
                "utm_content": "колесо фортуны",
                "utm_term": data.get("utm_term", "")
            }

            response = requests.post(WORDPRESS_API_URL, data=wordpress_data)

            if response.status_code == 200:
                print("✅ Лид успешно отправлен в WordPress!")
                return JsonResponse({"success": True, "message": "Лид отправлен в WordPress"})
            else:
                print("❌ Ошибка при отправке в WordPress:", response.text)
                return JsonResponse({"success": False, "error": "Ошибка при отправке в WordPress"}, status=500)

        except Exception as e:
            print("❌ Ошибка сервера:", str(e))
            return JsonResponse({"success": False, "error": "Ошибка сервера"}, status=500)

    return JsonResponse({"success": False, "error": "Метод не разрешен"}, status=405)

from fastapi import APIRouter, Form, BackgroundTasks, status

router_email = APIRouter()

# Função para enviar notificação por email
async def write_notification(email: str, message=""):
    with open("log.txt", mode="a") as email_file:
        content = f"notification for {email}: {message}\n"
        email_file.write(content)

@router_email.post(
    path="/send-notification/email",
    status_code=status.HTTP_200_OK,
    response_description="Send message email",
    description="Route send message email",
    name="Route send message email"
)
async def send_notification(background_tasks: BackgroundTasks,email = Form(...,description="Email", title="Email")):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
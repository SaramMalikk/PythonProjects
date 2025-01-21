# from winotify import audio, Notification
# notification = Notification(
#     app_id="NeuralNine Script",
#     title="Reminder",
#     msg="Drink water",
#     duration="short"
# )
# notification.show()


# from onesignal import OneSignal, SegmentNotification
#
# client = OneSignal("7d93ba4b-3836-4625-9c77-e4c14e5e6af7", "os_v2_app_pwj3uszygzdclhdx4tau4xtk64jg2mcqguze5delueb7nr54qaqyhpqv3j77tozq3lqgds7iz2xlyrbeth6ucjve6ff4evar35zjzrq")
# notification_to_all_users = SegmentNotification(
#     contents={
#         "en": "Hello from OneSignal-Notifications"
#     },
#     included_segments=[SegmentNotification.ALL]
# )
# client.send(notification_to_all_users)


# import requests
#
# # OneSignal API endpoint
# url = "https://onesignal.com/api/v1/notifications"
#
# # Define the payload
# payload = {
#     "app_id": "7d93ba4b-3836-4625-9c77-e4c14e5e6af7",  # Replace with your OneSignal App ID
#     "included_segments": ["Subscribed Users"],  # Target subscribed web users
#     "contents": {"en": "Hello, this is a notification for your Web App!"},
#     "chrome_web_icon": "https://your-website.com/icon.png"  # Optional: Notification icon
# }
#
# # Define headers
# headers = {
#     "Content-Type": "application/json; charset=utf-8",
#     "Authorization": f"os_v2_app_pwj3uszygzdclhdx4tau4xtk64jg2mcqguze5delueb7nr54qaqx5z4wf26rzitqhgczfgls7vefdoyi6qgtw7v2bphoff2o4fwelma"  # Replace with your REST API Key
# }
#
# # Send the request
# response = requests.post(url, json=payload, headers=headers)
#
# print("Notification response:", response.json())
#
# from plyer import notification
# import time
#
# if __name__ == "__main__":
#     try:
#         while True:
#             notification.notify(
#                 title="Hello",
#                 message="Hi, this is your notification!",
#                 app_icon="/Users/khizar/Downloads/water.png",  # Provide a valid path to the icon
#                 timeout=5  # Time in seconds
#             )
#             time.sleep(6)  # Delay between notifications
#     except Exception as e:
 #         print(f"Error: {e}")

from pync import Notifier
import time

try:
    while True:
        Notifier.notify(
            title="Notification from Python.",
            message="Happy Coding!",
            appIcon="/Users/khizar/Downloads/water.png"  # Provide a valid icon path
            )
        delay_time_min = 60
        time.sleep(delay_time_min * 60)  # Delay between notifications
except Exception as e:
    print(f"Error: {e}")


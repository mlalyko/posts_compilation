import vk_api
from cred import login, password, groups, my_community
from datetime import date, datetime, timedelta


def main():
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    groups_info = vk.groups.getById(group_ids=groups)
    posts_to_publish = {}

    for group in groups_info:
        response = vk.wall.get(owner_id=f'-{group["id"]}', count=10, filter='owner')
        posts_to_publish.update({group["id"]: {}})

        for post in response["items"]:
            if date.fromtimestamp(post["date"]) == (datetime.now() - + timedelta(days=1)).date():
                text = (f'• [https://vk.com/club{group["id"]}|{group["name"]}]:\n'
                        f'{post["text"]}\n\n'
                        f'------------------\n\n'
                        )

                attachment = ''

                for attach in post["attachments"]:
                    if attach["type"] == 'photo':
                        attachment = f'{attach["type"]}{attach["photo"]["owner_id"]}_{attach["photo"]["id"]}'
                        break

                posts_to_publish[group["id"]].update({post["id"]: {"text": text, "attachment": attachment}})

    main_text = 'Новости отечественных издательств, магазинов и тематических групп\n'
    main_attachment = ''
    publish_date = (datetime.now() + timedelta(hours=1)).timestamp()

    for i in posts_to_publish.values():
        for j in i.values():
            main_text += j.pop("text")
            if j["attachment"]:
                main_attachment += f'{j.pop("attachment")},'

            if main_attachment.count(',') == 10:
                vk.wall.post(owner_id=my_community, from_group=1, message=main_text, attachments=main_attachment,
                             publish_date=publish_date)
                main_text = 'Новости отечественных издательств, магазинов и тематических групп\n'
                main_attachment = ''

    vk.wall.post(owner_id=-120965961, from_group=1, message=main_text,
                 attachments=main_attachment, publish_date=publish_date)


if __name__ == '__main__':
    main()

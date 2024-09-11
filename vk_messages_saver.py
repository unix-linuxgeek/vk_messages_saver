import vk_api
import time

token = "your access token"
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def choose_id_name():
    local_self_id = int(input("Enter SELF_ID number:   "))
    local_user_id = int(input("Enter USER_ID number:   "))
    local_self_name = input("Enter SELF_ID name:   ")
    local_user_name = input("Enter USER_ID name:   ")
    local_names = {local_self_id: local_self_name, local_user_id: local_user_name}
    print(
        f"Message history with {local_self_name}:{local_self_id} and {local_user_name}:{local_user_id} will be "
        f"downloaded in a few minutes")
    return local_self_id, local_user_id, local_self_name, local_user_name, local_names


def get_dialog(local_user_id, sleep_time=1):
    print(sleep_time)
    local_dialog = vk.messages.getHistory(user_id=user_id)
    time.sleep(sleep_time)
    dialog_len = local_dialog['count']
    print(dialog_len)
    local_history = []

    if dialog_len > 200:
        resid = dialog_len
        offset = 0
        while resid > 0:
            hist = vk.messages.getHistory(
                user_id=local_user_id,
                count=200,
                offset=offset,
                rev=1)

            local_history.append(hist)

            time.sleep(sleep_time)
            resid -= 200
            offset += 200
            if resid > 0:
                print(f'--processing {local_user_id}: {resid} of {dialog_len} messages left')

    return local_history


def format_history_messages(local_history, local_names):
    res = ''
    for item in local_history['items']:
        name = local_names[item['from_id']]
        res += name + ':\n' + item['text'] + '\n'
        res += '-----------------------------------\n'
    return res


def file_name(local_self_name, local_user_name):
    local_file = "message history " + local_self_name + " and " + local_user_name
    return local_file


def save_to_file(local_dialog, local_names, local_file):
    with open(local_file, 'w', encoding='utf-8') as f:
        for history in local_dialog:
            s = format_history_messages(history, local_names)
            f.write(s)


self_id, user_id, self_name, user_name, names = choose_id_name()
print(names)
dialog = get_dialog(user_id)
file = file_name(self_name, user_name)
save_to_file(dialog, names, file)

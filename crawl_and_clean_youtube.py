import os
import sys
import json
import subprocess
from tqdm import tqdm


def get_channel(link,outdir):
    '''
    Get livechat and comment data from a given channel
    '''
    if link.endswith('/'):
        link = link[:-1]
        
    command_video = ['yt-dlp', '-ciw', '-o', os.path.join(outdir,"%(release_timestamp)s==%(id)s==%(duration)s==%(channel_follower_count)s==%(view_count)s"), '--write-comments', '--download-archive', 'archive.txt', '--write-info-json', '--no-warnings', '--no-progress', '-N', '4',
              '--skip-download', '--all-subs', link+'/videos']
    subprocess.call(command_video)
    
    command_short = ['yt-dlp', '-ciw', '-o', os.path.join(outdir,"%(release_timestamp)s==%(id)s==%(duration)s==%(channel_follower_count)s==%(view_count)s"), '--write-comments', '--download-archive', 'archive.txt', '--write-info-json', '--no-warnings', '--no-progress', '-N', '4',
              '--skip-download', '--all-subs', link+'/shorts']
    subprocess.call(command_short)
    
    
    command_stream = ['yt-dlp', '-ciw', '-o', os.path.join(outdir,"%(release_timestamp)s==%(id)s==%(duration)s==%(channel_follower_count)s==%(view_count)s"), '--write-comments', '--download-archive', 'archive.txt', '--write-info-json', '--no-warnings', '--no-progress', '-N', '4',
              '--skip-download', '--all-subs', link+'/streams']
    subprocess.call(command_stream)
    
    

def get_chat(json_data):
    
    full_data = json.loads(json_data)
    
    result = {}
    try:
        result['videoOffsetTimeMsec'] = full_data['replayChatItemAction']['videoOffsetTimeMsec']
    except:
        pass
    
    if "addChatItemAction" in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = "addChatItemAction"
    elif "addLiveChatTickerItemAction" in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = "addLiveChatTickerItemAction"
    elif "addBannerToLiveChatCommand" in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = "addBannerToLiveChatCommand"
    elif 'showLiveChatActionPanelAction' in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = 'showLiveChatActionPanelAction'
        result['chat_action'] = chat_action
        return result # this is usually a poll that shows up when the video is live
    elif 'updateLiveChatPollAction' in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = 'updateLiveChatPollAction'
        result['chat_action'] = chat_action
        return result # this is usually a poll that shows up when the video is live'updateLiveChatPollAction'
    elif 'removeChatItemAction' in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = 'removeChatItemAction'
        result['chat_action'] = chat_action
        return result
    elif "removeBannerForLiveChatCommand" in full_data['replayChatItemAction']['actions'][0].keys():
        chat_action = 'removeBannerForLiveChatCommand'
        result['chat_action'] = chat_action
        return result
    
    result['chat_action'] = chat_action

    if 'item' not in full_data['replayChatItemAction']['actions'][0][chat_action].keys():
        render = 'liveChatBannerRenderer' # this message is pinned
        chat = full_data['replayChatItemAction']['actions'][0][chat_action]['bannerRenderer']['liveChatBannerRenderer']['contents']['liveChatTextMessageRenderer']
    else:
        if 'liveChatTickerPaidMessageItemRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatTickerPaidMessageItemRenderer'
        elif 'liveChatPaidMessageRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatPaidMessageRenderer'
        elif 'liveChatPaidStickerRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatPaidStickerRenderer'
        elif 'liveChatTextMessageRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatTextMessageRenderer'
        elif 'liveChatMembershipItemRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatMembershipItemRenderer'
        elif 'liveChatTickerSponsorItemRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatTickerSponsorItemRenderer'
        elif 'liveChatTickerPaidStickerItemRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatTickerPaidStickerItemRenderer'
        elif 'liveChatModeChangeMessageRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():    
            render = "liveChatModeChangeMessageRenderer"
        elif 'liveChatSponsorshipsGiftPurchaseAnnouncementRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():   
            render = 'liveChatSponsorshipsGiftPurchaseAnnouncementRenderer'
        elif 'liveChatSponsorshipsGiftRedemptionAnnouncementRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():
            render = 'liveChatSponsorshipsGiftRedemptionAnnouncementRenderer'
        elif 'liveChatPlaceholderItemRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys():    
            render = 'liveChatPlaceholderItemRenderer'
        elif 'liveChatViewerEngagementMessageRenderer' in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys(): 
            render = 'liveChatViewerEngagementMessageRenderer'
        elif "liveChatActionPanelRenderer" in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys(): 
            render = "liveChatActionPanelRenderer"
        elif "liveChatDonationAnnouncementRenderer" in full_data['replayChatItemAction']['actions'][0][chat_action]['item'].keys(): 
            render = "liveChatDonationAnnouncementRenderer"
        chat = full_data['replayChatItemAction']['actions'][0][chat_action]['item'][render]
    
    try:
        result['message_duration'] = chat['durationSec']
    except:
        pass
    
    if 'showItemEndpoint' in chat.keys():
        chat = chat['showItemEndpoint']['showLiveChatItemEndpoint']['renderer']
        if 'liveChatMembershipItemRenderer' in chat.keys():
            chat = chat['liveChatMembershipItemRenderer']
        elif 'liveChatPaidMessageRenderer' in chat.keys():
            chat = chat['liveChatPaidMessageRenderer']
        elif 'liveChatPaidStickerRenderer' in chat.keys():
            chat = chat['liveChatPaidStickerRenderer']
        elif 'liveChatSponsorshipsGiftPurchaseAnnouncementRenderer' in chat.keys():    
            chat = chat['liveChatSponsorshipsGiftPurchaseAnnouncementRenderer']
            if 'header' in chat.keys():
                chat = chat['header']
                if 'liveChatSponsorshipsHeaderRenderer' in chat.keys():
                    chat = chat['liveChatSponsorshipsHeaderRenderer']
            
    result['chat_type'] = render.replace('liveChat','').replace('Renderer','')
    
    
    message = ''
    if 'message' in chat.keys():
        message = 'message'
    elif 'text' in chat.keys():
        message = 'text'
    elif 'primaryText' in chat.keys():
        message = 'primaryText'
    if message != '':
        result['message'] = []
        if 'runs' in chat[message].keys():
            for i in chat[message]['runs']:
                if 'text' in i.keys():
                    result['message'].append({'text':i['text']})
                elif 'emoji' in i.keys():
                    emoji = {'emoji_id':i['emoji']['emojiId']}
                    if 'shortcuts' in i['emoji'].keys():
                        emoji['shortcuts'] = i['emoji']['shortcuts'][0]
                    if 'isCustomEmoji' in i['emoji'].keys():
                        emoji['custom_emoji'] = i['emoji']['isCustomEmoji']
                    result['message'].append(emoji)
    elif 'sticker' in chat.keys():
        result['sticker'] = chat['sticker']['accessibility']['accessibilityData']['label']
    try:    
        result['author_name'] = chat['authorName']['simpleText']
    except:
        pass
    try:
        result['purchase_amount'] = chat["purchaseAmountText"]["simpleText"]
        result['superchat'] = True
    except:
        result['superchat'] = False

    try:
        result['timestamp_usec'] = chat['timestampUsec']
    except:
        pass
    try:
        result['video_time'] = chat['timestampText']['simpleText']
    except:
        pass
    try:
        result['author_badge'] = chat['authorBadges'][0]['liveChatAuthorBadgeRenderer']['tooltip']
    except:
        pass

    return result



def clean_live_chat(data_path):
    out_path = data_path + '.out'
    with open(out_path,'w') as out:
        with open(data_path,'r') as f:
            for i,item in tqdm(enumerate(f.readlines())):
                if 'isLive' in json.loads(item).keys():
                    if json.loads(item)['isLive']:
                        return
                    else:
                        pass
                result = get_chat(item)
                out.write(json.dumps(result)+'\n')
    os.remove(data_path)
    
    
    
columns = {'id', 'title', 'thumbnail', 'description', 'uploader', 'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'duration', 'view_count', 'age_limit', 'webpage_url', 'categories', 'tags',  'live_status', 'release_timestamp', 'comment_count', 'like_count', 'channel', 'channel_follower_count', 'upload_date', 'availability', 'webpage_url_basename', 'webpage_url_domain', 'playlist_count', 'playlist', 'playlist_id', 'playlist_title', 'playlist_uploader', 'playlist_uploader_id', 'playlist_index', 'display_id', 'fulltitle', 'duration_string', 'release_date', 'is_live', 'was_live', 'comments', 'url', 'language_preference'}


def clean_info(data_path):
    '''
    clean meta json file
    '''
    out_path = data_path + '.out'
    with open(data_path,'r') as f:
        content = json.loads(f.read())
        new = {}
        for k in content.keys():
            if k in columns:
                new[k] = content[k]
        with open(out_path,'w') as out:
            out.write(json.dumps(new))
            
    os.remove(data_path)

    

if __name__ == "__main__":
    
    vtuber = sys.argv[1]
    link = sys.argv[2]
    outdir = sys.argv[3]
    print(outdir)
    
    outdir = os.path.join(outdir,vtuber)
    
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    
    if not os.path.exists(os.path.join(outdir,'done')):
        get_channel(link,outdir)

        live_chats = [i for i in os.listdir(outdir) if 'live_chat' in i and 'out' not in i]

        if len(live_chats) > 0:
            for chat in tqdm(live_chats):
                clean_live_chat(os.path.join(outdir,chat))

        infos = [i for i in os.listdir(outdir) if 'info' in i and 'out' not in i]

        if len(infos) > 0:
            for info in tqdm(infos):
                clean_info(os.path.join(outdir,info))


        with open(os.path.join(outdir,'done'),'w') as out:
            out.write('done')
    
    else:
        print('skipping')
    
#!/usr/bin/python3

import argparse
import logging
import shutil
import eyed3
import glob
import os

# script defaults
collection_path = "/media/sean/GoFlex Home/music/tech & house"
unorganised_path = "/media/sean/GoFlex Home/music" #/inbox/soundcloud/new"
logfile_path = "/home/sean/logs/organise.log"
sort_tag = "album"
deli = ","
del_tag = "del"
rate_tag = "s"

# dictionary with the full dir names
dir_name = {"ac": "acid", "ba": "base", "bo": "bouncy", "da": "dance", "de": "deep", "di": "disco", "dr": "drum & base", "ga": "garage", "ge": "gem", "kb": "k&b", "ml": "mellow", "md": "melodic", "po": "pop", "th": "tech house", "te": "techno", "tr": "trance"}
# dictonary with sub dir's 
sub_name = {"da": "dark", "dab": "dark (beat)", "de": "deep", "dep": "deep (beat)", "ge": "gem", "geb": "gem (beat)", "hi": "high", "hib": "high (beat)", "lo": "low", "lob": "low (beat)", "mi": "mid", "mib": "mid (beat)", "ro": "rolling","lf": "lofi", "lfb": "lofi (beat)", "po": "pop", "bo": "bouncy"}


def get_args():
    """
    Function will return command line ags
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--unorganised", help="Specify the path with your unorganised music", type=str, default=unorganised_path)
    parser.add_argument("-c", "--collection", help="Specify the path with your music collection", type=str, default=collection_path)
    parser.add_argument("-t", "--tag", help="set the tag you ", type=str, default=sort_tag)
    parser.add_argument("-d", "--delimiter", help="Set the delimiter used to separate parameters in your tag", type=str, default=deli)
    # return args
    return parser.parse_args()


def get_dir_files(path, log):
    """
    Fucntion will return the files in a given directory as a list
    """
    files = glob.iglob(path + "/**", recursive=True)
    #log.debug("checking dir {path} and found {num} files".format(path=path, num=len(files)))
    return files

def get_song_tags(song_path, tag_to_check, delimiter):
    """
    Function returns the value in the tag passed to the function in a list created using the specified delimiter
    """
    tag_list = None
    try:
        # get the data in the ID£ tag
        tag_list = get_tag_object(song_path, tag_to_check)
        tag_list = tag_list.split(delimiter)
    except AttributeError:
        # there's a chance the song hasn't been tagged yet or not a music file, just skip
        pass
    # return the tag
    return tag_list


def get_tag_object(song_path, tag_to_check):
    """
    Function returns an object for a songs tag
    """
    tag_obj = None
    try:
        if os.path.isfile(song_path):
            song = eyed3.load(song_path)
            tag_obj = getattr(song.tag, tag_to_check)
    except OSError:
        pass
    # return the object
    return tag_obj


def set_tag_value(song_path, tag, value):
    """
    Function will set value for a tag
    """
    tag_set = False
    #song = eyed3.load(song_path)
    print("ssong is {}".format(song_path))
    tag = getattr(song_path, tag)
    print("tag attr is {} and value is {}".format(tag, value))
    if tag:
        tag = value
        song_path.tag.save()
        tag_set = True

    return tag_set


def get_new_dir(tag):
    """
    Function extracts the directory from the tag
    """
    new_dir = None
    top_dir_key = tag[:2]
    sub_dir_key = tag[2:]
    # check dictionaries for dir names and extract address
    try:
        new_dir = "{top}/{sub}".format(top=dir_name[top_dir_key], sub=sub_name[sub_dir_key])
    except KeyError:
        pass

    return new_dir


def main():
    """
    do all the things
    """
    # create logger with app_name and set level
    logger = logging.getLogger("organise")
    logger.setLevel(logging.DEBUG)
    file_hand = logging.FileHandler(logfile_path)
    file_hand.setLevel(logging.DEBUG)
    # set format for message output
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_hand.setFormatter(formatter)
    logger.addHandler(file_hand)
    logger.info("*********************************************************************************************")
    logger.info("                                       log start                                             ")
    logger.info("*********************************************************************************************")
    # get args if any or use defaults
    args = get_args()
    # change the current dir 
    os.chdir(args.unorganised)
    # get a list of files to run the sort on 
    file_list = get_dir_files(args.unorganised, logger)
    # debug line
    print("found following files {}".format(file_list))
    # loop through files and print tags
    for tune in file_list:
        tags = get_song_tags(tune, args.tag, args.delimiter)
        if os.path.isfile(tune):
            song_obj = eyed3.load(tune)
        else:
            print("{file} is not file".format(file=tune))
        if tags:
            print("Found tags {tags} for {song}".format(tags=tags, song=tune))
            # process tags from list
            for tag in tags:
                tag_lower = tag.lower()
                tag_len = len(tag_lower)
                # check if command is delete
                if tag_lower == del_tag:
                    print("Deleting file {file}".format(file=tune))
                    os.remove(tune)
                # check is command is move
                if tag_len >= 4:
                    # check if command is nove
                    new_addr = get_new_dir(tag_lower)
                    print("extracted address is {}".format(new_addr))
                    if new_addr:
                        # get file name 
                        name = tune.split("/")[-1]
                        # get the new address
                        new_addr = "{base}/{folder}/{name}".format(base=args.collection, folder=new_addr, name=name)
                        print("new address is {} and file name is {}".format(new_addr, name))
                        # write any remaining tags to file
                        tags.remove(tag)
                        # TODO set tag not working for now 
                        #set_tag_value(tune, args.tag, tag_lower)
                        # move file
                        #tune = "{}/{}".format(args.unorganised, tune)
                        shutil.move(tune, new_addr)
                # check if command is rating
                if tag_len == 2 and tag.startswith(rate_tag):
                    rating = int(tag_lower[1:])
                    song_obj.tag.track_num = rating
                    song_obj.tag.save()
                    set_rate = song_obj.tag.track_num
                    print("rating for {song} set to {rate}".format(song=tune, rate=set_rate))

                else:
                    logger.info("Couldn't process tag \"{tag}\" in {song}".format(tag=tag, song=tune))


main()

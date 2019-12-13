import pafy
import sys
import re
import urllib.request
import urllib.parse
import webbrowser

def main():
	comm_type = sys.argv[1]
	if(comm_type == '--get' or comm_type == '-g'):
		vid = pafy.new(sys.argv[2])
		print('\nTITLE    : ' + vid.title)
		print('AUTHOR   : ' + vid.author)
		print('DURATION : ' + vid.duration)
		print('LIKES    : ' + str(vid.likes))
		print('DISLIKES : ' + str(vid.dislikes))
		print('\n')
	elif(comm_type == '--download' or comm_type == '-d'):
		if(sys.argv[2] == '--audio' or sys.argv[2] == '-a'):
			vid = pafy.new(sys.argv[3])
			audio_file = vid.getbestaudio()
			audio_file.download()
		elif(sys.argv[2] == '--video' or sys.argv[2] == '-v'):
			if(len(sys.argv) == 4):
				vid = pafy.new(sys.argv[3])
				vid_file = vid.getbest()
				vid_file.download()
			elif(len(sys.argv) == 5):
				vid = pafy.new(sys.argv[3])
				vid_file = vid.streams
				for stream in vid_file:
					if(stream.resolution.split('x')[1] == sys.argv[4].split('--')[1].split('p')[0]):
						print('DOWNLOADING RESOLUTION %s' % (stream.resolution))
						stream.download()
	elif(comm_type == '--search' or comm_type == '-s'):
		if(len(sys.argv) == 2):
			query_string = urllib.parse.urlencode({"search_query" : input('Enter Search Query  : ')})
			html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
			search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
			counter = 0
			for video in search_results:
				search_results[counter] = 'https://www.youtube.com/watch?v='+video
				vid = pafy.new('https://www.youtube.com/watch?v='+video)
				print('-'*25)
				print('TITLE    : ' + vid.title)
				print('AUTHOR   : ' + vid.author)
				print('DURATION : ' + vid.duration)
				print('LIKES    : ' + str(vid.likes))
				print('DISLIKES : ' + str(vid.dislikes))
				counter += 1
				if(counter == 5): break
			comm = input('[E]xit, [D]ownload [index of video] or [O]pen : ')
			if(comm[0] == 'd' or comm == 'D'):
				media_type = input('[A]udio or [V]ideo : ')
				if(media_type == 'a' or media_type == 'A'):
					vid = pafy.new(search_results[int(comm.split()[1])]-1)
					vid_file = vid.getbestaudio()
					vid_file.download()
				elif(media_type == 'v' or media_type == 'V'):
					vid = pafy.new(search_results[int(comm.split()[1])]-1)
					vid_file = vid.getbest()
					vid_file.download()
			elif(comm[0] == 'e' or comm == 'E'): return
			elif(comm[0] == 'o' or comm == 'O'):
				webbrowser.open(search_results[int(comm.split()[1])]-1)


if __name__ == '__main__':
	main()
#!/usr/bin/env python3.5
""" small program to split preprocessed translation units into more human-readable source-like files. """
import os
import pdb

if __name__=="__main__":
	# scripts is a dictionary mapping file names to source files
	# it is created by reading through the preprocessed file using the preprocessor lines and stack discipline
	# it is used for compressing #include preprocessor directives
	scripts = {}
	# the empty stack will be a null string
	key = ""
	pdb.set_trace()
	with open("hello.E") as f:
		# with the opened preprocessed C file
		for l in f:
			if l.startswith("#"):
				# if the line starts with a hash we can assume that the stack of the macro machine is pushing
				# since the preprocessor resolves all other tokens beginning with #, we don't have to worry about erroneous matches
				line = l.split(' ')
				if len(line) == 3:
					_, line_num, filename = line
					flags = []
				else:
					_, line_num, filename, *flags = line
					flags = [i.strip('\n') for i in flags]
				print(l)
				print(key, filename, flags)
				if "1" in flags or flags == [] or "3" in flags or key == "":
					# the filename is the name of the next included file
					# or this is the base file being preprocessed
					# this is the file being pushed on the expander's stack
					key = filename
					print("Pushing: {}\n".format(key))
				if "2" in flags:
					# the filename is the name of the file being returned to
					# the filename is the file popped from the top of the expander's stack
					# reduce the previously missing lines to a patched include statement
					# pdb.set_trace()
					scripts.setdefault(filename, list()).append("#include {}\n".format(key))
					# and change the key to point to the current filename
					key = filename
					print("Popping: {}\n".format(key))

			else:
				# otherwise l is a line of unexpanded source
				# add this line to the text of the current file on the stack
				# pdb.set_trace()
				scripts.setdefault(key, list()).append(l)
	# once we parse the preprocessed file, we can write out the results to a directory
	res_dir = "./res"
	# os.mkdir("./res")
	pdb.set_trace()
	for k in scripts:
		with open("{}/{}".format(res_dir, k.replace("/","_").strip('"')), "w") as res:
			res.write(''.join(scripts[k]))

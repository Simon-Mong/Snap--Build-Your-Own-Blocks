#!/usr/bin/env python

import cgi
import sys
import stitchcode
import time
import hashlib

pixels_per_millimeter = 10

def main():
	emb = stitchcode.Embroidery()
	data = cgi.FieldStorage();	
	xarr = data.getlist("x[]")
	yarr = data.getlist("y[]")
	jarr = data.getlist("j[]")
	lx = -99999999
	ly = -99999999
	
	fid = str(int(time.time() * 1000))
	#sys.stderr.write(hashlib.sha1(str(time.time())).hexdigest())
		
	for i in range(0, len(xarr)):
		x = int(xarr[i])
		y = int(yarr[i])*-1;
		if jarr[i] == "true":
			j = True
		else:
			j = False
			
		if not(x == lx and y == ly):
			emb.addStitch(stitchcode.Point(x,y,j))
		lx = x
		ly = y
		
	emb.translate_to_origin()	
	emb.flatten()
	emb.scale(27.80/pixels_per_millimeter)
	emb.add_endstitches_to_jumps(10)
	#emb.to_triple_stitches()	
	emb.save_as_png("files/%s.png" % fid)
	emb.save_as_exp("files/%s.exp" % fid)
	
	print "Content-Disposition: attachment; filename=%s.exp" % fid	
	print "Content-Type: application/octet-stream\n"
	print emb.export_melco()

main()

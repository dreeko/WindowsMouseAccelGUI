import winreg
import struct
import pandas as pd
import numpy as np
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
mouse_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", 0, winreg.KEY_READ)
x_key = winreg.QueryValueEx(mouse_key, 'SmoothMouseXCurve')
y_key = winreg.QueryValueEx(mouse_key, 'SmoothMouseYCurve')
x_res_list = []
y_res_list = []


b_picked = False
b_dragging = False
current_artist = None
current_artist_ind = None
count_update_tick = 0
threshold_update_tick_to_draw = 10


fig, ax = plt.subplots()
aa = np.linspace(0,40,num=400)
ax.set_xbound(-5,45)
ax.set_ybound(-5,475)	



def encode_reg(new_x_coords, new_y_coords):
	pass

def decode_reg(in_reg_key, ch_res_list):
	for i in (range(35,0,-8)):
		h_reg_key_1 = in_reg_key[0][i-1:i+1][::-1].hex() 
		h_reg_key_2 = in_reg_key[0][i-3:i-1][::-1].hex() 
		f_res = float(str(int(h_reg_key_1, 16)) + '.' + str(int(h_reg_key_2, 16)));
		ch_res_list.append(f_res)

	ch_res_list.reverse()

def onpick(event):
	global b_picked
	global current_artist
	global current_artist_ind
	if (not b_picked):
		current_artist = event.artist
		xdata, ydata = current_artist.get_xdata(), current_artist.get_ydata()
		current_artist_ind = event.ind
		b_picked = True
	else:
		pass

def onmotion(event):
	global current_artist
	global b_picked
	global count_update_tick
	global threshold_update_tick_to_draw
	if (b_picked):
		b_dragging = True
		xpress, ypress = event.xdata,event.ydata
		art_xdata, art_ydata = current_artist.get_xdata(), current_artist.get_ydata()
		art_xdata[current_artist_ind], art_ydata[current_artist_ind] = xpress, ypress
		current_artist.set_xdata(art_xdata)
		current_artist.set_ydata(art_ydata)
		count_update_tick += 1
		if (count_update_tick >= threshold_update_tick_to_draw):
			count_update_tick = 0
			interp_and_draw(art_xdata, art_ydata)

def onrelease(event):
	global b_picked
	global current_artist

	if(current_artist is not None):
		interp_and_draw(current_artist.get_xdata(), current_artist.get_ydata())
	b_picked = False

def interp_and_draw(xvals, yvals):
	global aa
	global fig
	global ax
	global count_update_tick

	uv_spline = interpolate.UnivariateSpline(xvals, yvals, k=3, ext=0, s = 0)
	lin_interp = interpolate.interp1d(xvals,yvals, kind='quadratic', fill_value='extrapolate')
	lin_points = lin_interp(aa)
	uv_interped_points = uv_spline(aa)
	ax.clear()
	ax.set_autoscale_on(False)
	ax.set_xbound(-5,45)
	ax.set_ybound(-5,475)

	
	#ax.plot(aa, uv_interped_points,'r')
	ax.plot(xvals, yvals, 'bo',picker=5)
	ax.plot(aa, lin_points, 'g')
	plt.draw()

def cb_save_reg_file():
	pass


decode_reg(x_key, x_res_list)
decode_reg(y_key,y_res_list)

fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('motion_notify_event', onmotion)
fig.canvas.mpl_connect('button_release_event', onrelease)
plt.rc('figure', figsize=(10, 5))

interp_and_draw( np.asarray(x_res_list), np.asarray(y_res_list) )
ax_save = plt.axes([0.81, 0.05, 0.1, 0.075])
butt_save = plt.Button(ax_save, 'Save')

butt_save.on_clicked(cb_save_reg_file)


plt.show()

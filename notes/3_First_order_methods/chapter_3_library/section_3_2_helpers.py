from autograd import grad as compute_grad   # The only autograd function you may ever need
import autograd.numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Annotation
from mpl_toolkits.mplot3d.proj3d import proj_transform
import math
import copy


# visualize derivatie
def compare_2d3d(func1,func2,**kwargs):
    # input arguments
    view = [20,-65]
    if 'view' in kwargs:
        view = kwargs['view']
        
    # define input space
    w = np.linspace(-3,3,200)                  # input range for original function
    if 'w' in kwargs:
        w = kwargs['w']
        
    # define pts
    pt1 = 0
    if 'pt1' in kwargs:
        pt1 = kwargs['pt1']
        
    pt2 = [0,0]
    if 'pt2' in kwargs:
        pt2 = kwargs['pt2']
    
    # construct figure
    fig = plt.figure(figsize = (6,3))
          
    # remove whitespace from figure
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # remove whitespace
    fig.subplots_adjust(wspace=0.01,hspace=0.01)
        
    # create subplot with 3 panels, plot input function in center plot
    gs = gridspec.GridSpec(1, 2, width_ratios=[1,2]) 
  
    ### draw 2d version ###
    ax1 = plt.subplot(gs[0]); 
    grad = compute_grad(func1)
    
    # generate a range of values over which to plot input function, and derivatives
    g_plot = func1(w)
    g_range = max(g_plot) - min(g_plot)             # used for cleaning up final plot
    ggap = g_range*0.2
    
    # grab the next input/output tangency pair, the center of the next approximation(s)
    pt1 = float(pt1)
    g_val = func1(pt1)

    # plot original function
    ax1.plot(w,g_plot,color = 'k',zorder = 1,linewidth=2)                          
    
    # plot the input/output tangency point
    ax1.scatter(pt1,g_val,s = 60,c = 'lime',edgecolor = 'k',linewidth = 2,zorder = 3)            # plot point of tangency

    #### plot first order approximation ####
    # plug input into the first derivative
    g_grad_val = grad(pt1)

    # compute first order approximation
    w1 = pt1 - 3
    w2 = pt1 + 3
    wrange = np.linspace(w1,w2, 100)
    h = g_val + g_grad_val*(wrange - pt1)

    # plot the first order approximation
    ax1.plot(wrange,h,color = 'lime',alpha = 0.5,linewidth = 3,zorder = 2)      # plot approx
    
    # make new x-axis
    ax1.plot(w,g_plot*0,linewidth=3,color = 'k')
    
    #### clean up panel ####
    # fix viewing limits on panel
    ax1.set_xlim([min(w),max(w)])
    ax1.set_ylim([min(min(g_plot) - ggap,-4),max(max(g_plot) + ggap,0.5)])

    # label axes
    ax1.set_xlabel('$w$',fontsize = 12,labelpad = -50)
    ax1.set_ylabel('$g(w)$',fontsize = 25,rotation = 0,labelpad = 50)
    
    ax1.grid(False)
    ax1.yaxis.set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    
    
    ### draw 3d version ###
    ax2 = plt.subplot(gs[1],projection='3d'); 
    grad = compute_grad(func2)
    w_val = [float(0),float(0)]
    
    # define input space
    w1_vals, w2_vals = np.meshgrid(w,w)
    w1_vals.shape = (len(w)**2,1)
    w2_vals.shape = (len(w)**2,1)
    w_vals = np.concatenate((w1_vals,w2_vals),axis=1).T
    g_vals = func2(w_vals) 
      
    # evaluation points
    w_val = np.array([float(pt2[0]),float(pt2[1])])
    w_val.shape = (2,1)
    g_val = func2(w_val)
    grad_val = grad(w_val)
    grad_val.shape = (2,1)  

    # create and evaluate tangent hyperplane
    w1tan_vals, w2tan_vals = np.meshgrid(w,w)
    w1tan_vals.shape = (len(w)**2,1)
    w2tan_vals.shape = (len(w)**2,1)
    wtan_vals = np.concatenate((w1tan_vals,w2tan_vals),axis=1).T

    #h = lambda weh: g_val +  np.dot( (weh - w_val).T,grad_val)
    h = lambda weh: g_val + (weh[0]-w_val[0])*grad_val[0] + (weh[1]-w_val[1])*grad_val[1]     
    h_vals = h(wtan_vals + w_val)

    # vals for cost surface, reshape for plot_surface function
    w1_vals.shape = (len(w),len(w))
    w2_vals.shape = (len(w),len(w))
    g_vals.shape = (len(w),len(w))
    w1tan_vals += w_val[0]
    w2tan_vals += w_val[1]
    w1tan_vals.shape =  (len(w),len(w))
    w2tan_vals.shape =  (len(w),len(w))
    h_vals.shape = (len(w),len(w))

    ### plot function ###
    ax2.plot_surface(w1_vals, w2_vals, g_vals, alpha = 0.5,color = 'w',rstride=25, cstride=25,linewidth=1,edgecolor = 'k',zorder = 2)

    ### plot z=0 plane ###
    ax2.plot_surface(w1_vals, w2_vals, g_vals*0, alpha = 0.1,color = 'w',zorder = 1,rstride=25, cstride=25,linewidth=0.3,edgecolor = 'k') 

    ### plot tangent plane ###
    ax2.plot_surface(w1tan_vals, w2tan_vals, h_vals, alpha = 0.4,color = 'lime',zorder = 1,rstride=50, cstride=50,linewidth=1,edgecolor = 'k')     

    # scatter tangency 
    ax2.scatter(w_val[0],w_val[1],g_val,s = 70,c = 'lime',edgecolor = 'k',linewidth = 2)
    
    ### clean up plot ###
    # plot x and y axes, and clean up
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False

    #ax2.xaxis.pane.set_edgecolor('white')
    ax2.yaxis.pane.set_edgecolor('white')
    ax2.zaxis.pane.set_edgecolor('white')

    # remove axes lines and tickmarks
    ax2.w_zaxis.line.set_lw(0.)
    ax2.set_zticks([])
    ax2.w_xaxis.line.set_lw(0.)
    ax2.set_xticks([])
    ax2.w_yaxis.line.set_lw(0.)
    ax2.set_yticks([])

    # set viewing angle
    ax2.view_init(view[0],view[1])

    # set vewing limits
    wgap = (max(w) - min(w))*0.4
    y = max(w) + wgap
    ax2.set_xlim([-y,y])
    ax2.set_ylim([-y,y])
    
    zmin = min(np.min(g_vals),-0.5)
    zmax = max(np.max(g_vals),+0.5)
    ax2.set_zlim([zmin,zmax])

    # label plot
    fontsize = 12
    ax2.set_xlabel(r'$w_1$',fontsize = fontsize,labelpad = -30)
    ax2.set_ylabel(r'$w_2$',fontsize = fontsize,rotation = 0,labelpad=-30)
        
    plt.show()

    
def show_stationary(func1,func2,func3,**kwargs):
    '''
    Input three functions, draw each highlighting their stationary points and draw tangent lines, mark evaluations on first derivative as well
    '''
        
    # define input space
    w = np.linspace(-3,3,5000)                  # input range for original function
    if 'w' in kwargs:
        w = kwargs['w']

    # construct figure
    fig = plt.figure(figsize = (7,5))
          
    # remove whitespace from figure
    #fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # remove whitespace
    fig.subplots_adjust(wspace=0.3,hspace=0.4)
       
    # create subplot with 3 panels, plot input function in center plot
    gs = gridspec.GridSpec(2, 3, width_ratios=[1,1,1]) 
  
    ###### draw function, tangent lines, etc., ######
    for k in range(3):
        ax = plt.subplot(gs[k]); 
        ax2 =  plt.subplot(gs[k+3],sharex=ax);  
        
        func = func1
        if k == 1:
            func = func2
        if k == 2:
            func = func3

        # generate a range of values over which to plot input function, and derivatives
        g_plot = func(w)
        grad = compute_grad(func)
        grad_plot = np.array([grad(s) for s in w])
        wgap = (max(w) - min(w))*0.1
        ggap = (max(g_plot) - min(g_plot))*0.1
        grad_gap = (max(grad_plot) - min(grad_plot))*0.1
        
        # plot first in top panel, derivative in bottom panel
        ax.plot(w,g_plot,color = 'k',zorder = 1,linewidth=2)   
        ax.set_title(r'$g(w)$',fontsize = 12)
        ax.set_xlim([min(w)-wgap,max(w)+wgap])
        ax.set_ylim([min(g_plot) - ggap, max(g_plot) + ggap])
        
        # plot derivative and horizontal axis
        ax2.plot(w,grad_plot,color = 'k',zorder = 1,linewidth = 2) 
        ax2.plot(w,grad_plot*0,color = 'k',zorder = 1,linewidth = 1,linestyle = '--') 
        ax2.set_title(r'$\frac{\mathrm{d}}{\mathrm{d}w}g(w)$',fontsize = 12)
        ax2.set_ylim([min(grad_plot) - grad_gap, max(grad_plot) + grad_gap])

        # clean up and label axes 
        ax.tick_params(labelsize=6)
        ax2.tick_params(labelsize=6)

        # determine zero derivative points 'visually'
        grad_station = copy.deepcopy(grad_plot)
        grad_station = np.sign(grad_station)
        ind = []
        for i in range(len(grad_station)-1):
            pt1 = grad_station[i]
            pt2 = grad_station[i+1]
            plot_pt1 = grad_plot[i]
            plot_pt2 = grad_plot[i+1]

            # if either point is zero add to list
            if pt1 == 0 or abs(plot_pt1) < 10**-5:
                ind.append(i)
            if pt2 == 0:
                ind.append(i+1)

            # if grad difference is small then sign change has taken place, add to list
            gap = abs(pt1 + pt2)
            if gap < 2 and pt1 !=0 and pt2 != 0:
                ind.append(i)

        # keep unique pts
        ind = np.unique(ind)
        
        # plot the input/output tangency points and tangent line
        wtan = np.linspace(-1,1,500)                  # input range for original function
        for pt in ind:
            # plot point
            w_val = w[pt]
            g_val = func(w_val)
            grad_val = grad(w_val)
            ax.scatter(w_val,g_val,s = 40,c = 'lime',edgecolor = 'k',linewidth = 2,zorder = 3)            # plot point of tangency
            ax2.scatter(w_val,grad_val,s = 40,c = 'lime',edgecolor = 'k',linewidth = 2,zorder = 3)            # plot point of tangency

            # plot tangent line in original space
            w1 = w_val - 1
            w2 = w_val + 1
            wrange = np.linspace(w1,w2, 100)
            h = g_val + 0*(wrange - w_val)
            ax.plot(wrange,h,color = 'lime',alpha = 0.5,linewidth = 1.5,zorder = 2)      # plot approx
    plt.show()
    




class Visualizer:
    '''
    Illustrate a run of your preferred optimization algorithm on a one or two-input function.  Run
    the algorithm first, and input the resulting weight history into this wrapper.
    ''' 
        
    ##### draw picture of function and run for two-input function ####       
    def two_input_contour_plot(self,g,w_hist,**kwargs):
        ##### construct figure with panels #####
        # construct figure
        fig = plt.figure(figsize = (10,4.5))
        
        # show original contour function as well?
        show_original = True
        if 'show_original' in kwargs:
            show_original = kwargs['show_original']

        # create figure with single plot for contour
        gs = gridspec.GridSpec(1, 2) 
        ax1 = plt.subplot(gs[0],aspect='equal'); 
        ax2 = plt.subplot(gs[1],aspect='equal'); 
        
        if show_original == False:
            gs = gridspec.GridSpec(1, 1) 
            ax2 = plt.subplot(gs[0],aspect='equal'); 

        # remove whitespace from figure
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # remove whitespace
        fig.subplots_adjust(wspace=0.01,hspace=0.01)
        
        ### make contour right plot - as well as horizontal and vertical axes ###
        self.contour_plot_setup(g,ax2,**kwargs)  # draw contour plot
        self.edgecolor = 'k'
        self.draw_weight_path(ax2,w_hist,**kwargs)        # draw path on contour plot
        
        if show_original == True:
            self.contour_plot_setup(g,ax1,**kwargs)  # draw contour plot

        # plot
        plt.show()

        
    ########################################################################################
    #### utility functions - for setting up / making contour plots, 3d surface plots, etc., ####
    # show contour plot of input function
    def contour_plot_setup(self,g,ax,**kwargs):
        xmin = -3.1
        xmax = 3.1
        ymin = -3.1
        ymax = 3.1
        if 'xmin' in kwargs:            
            xmin = kwargs['xmin']
        if 'xmax' in kwargs:
            xmax = kwargs['xmax']
        if 'ymin' in kwargs:            
            ymin = kwargs['ymin']
        if 'ymax' in kwargs:
            ymax = kwargs['ymax']      
        num_contours = 20
        if 'num_contours' in kwargs:
            num_contours = kwargs['num_contours']   
            
        # choose viewing range using weight history?
        if 'view_by_weights' in kwargs:
            view_by_weights = True
            weight_history = kwargs['weight_history']
            if view_by_weights == True:
                xmin = min([v[0] for v in weight_history])[0]
                xmax = max([v[0] for v in weight_history])[0]
                xgap = (xmax - xmin)*0.25
                xmin -= xgap
                xmax += xgap

                ymin = min([v[1] for v in weight_history])[0]
                ymax = max([v[1] for v in weight_history])[0]
                ygap = (ymax - ymin)*0.25
                ymin -= ygap
                ymax += ygap
 
        ### plot function as contours ###
        self.draw_contour_plot(g,ax,num_contours,xmin,xmax,ymin,ymax)
        
        ### cleanup panel ###
        ax.set_xlabel('$w_0$',fontsize = 14)
        ax.set_ylabel('$w_1$',fontsize = 14,labelpad = 15,rotation = 0)
        ax.axhline(y=0, color='k',zorder = 0,linewidth = 0.5)
        ax.axvline(x=0, color='k',zorder = 0,linewidth = 0.5)
        # ax.set_xticks(np.arange(round(xmin),round(xmax)+1))
        # ax.set_yticks(np.arange(round(ymin),round(ymax)+1))
        
        # set viewing limits
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymin,ymax)

    ### function for creating contour plot
    def draw_contour_plot(self,g,ax,num_contours,xmin,xmax,ymin,ymax):
        #### define input space for function and evaluate ####
        w1 = np.linspace(xmin,xmax,400)
        w2 = np.linspace(ymin,ymax,400)
        w1_vals, w2_vals = np.meshgrid(w1,w2)
        w1_vals.shape = (len(w1)**2,1)
        w2_vals.shape = (len(w2)**2,1)
        h = np.concatenate((w1_vals,w2_vals),axis=1)
        func_vals = np.asarray([ g(np.reshape(s,(2,1))) for s in h])

        w1_vals.shape = (len(w1),len(w1))
        w2_vals.shape = (len(w2),len(w2))
        func_vals.shape = (len(w1),len(w2)) 
        
        ### make contour right plot - as well as horizontal and vertical axes ###
        # set level ridges
        levelmin = min(func_vals.flatten())
        levelmax = max(func_vals.flatten())
        cutoff = 1
        cutoff = (levelmax - levelmin)*cutoff
        numper = 4
        levels1 = np.linspace(cutoff,levelmax,numper)
        num_contours -= numper

        # produce generic contours
        levels2 = np.linspace(levelmin,cutoff,min(num_contours,numper))
        levels = np.unique(np.append(levels1,levels2))
        num_contours -= numper
        while num_contours > 0:
            cutoff = levels[1]
            levels2 = np.linspace(levelmin,cutoff,min(num_contours,numper))
            levels = np.unique(np.append(levels2,levels))
            num_contours -= numper
   
        # plot the contours
        ax.contour(w1_vals, w2_vals, func_vals,levels = levels[1:],colors = 'k')
        ax.contourf(w1_vals, w2_vals, func_vals,levels = levels,cmap = 'Blues')

        ###### clean up plot ######
        ax.set_xlabel('$w_0$',fontsize = 12)
        ax.set_ylabel('$w_1$',fontsize = 12,rotation = 0)
        ax.axhline(y=0, color='k',zorder = 0,linewidth = 0.5)
        ax.axvline(x=0, color='k',zorder = 0,linewidth = 0.5)
        
        
    ### makes color spectrum for plotted run points - from green (start) to red (stop)
    def make_colorspec(self,w_hist):
        # make color range for path
        s = np.linspace(0,1,len(w_hist[:round(len(w_hist)/2)]))
        s.shape = (len(s),1)
        t = np.ones(len(w_hist[round(len(w_hist)/2):]))
        t.shape = (len(t),1)
        s = np.vstack((s,t))
        colorspec = []
        colorspec = np.concatenate((s,np.flipud(s)),1)
        colorspec = np.concatenate((colorspec,np.zeros((len(s),1))),1)
        return colorspec

    ### function for drawing weight history path
    def draw_weight_path(self,ax,w_hist,**kwargs):
        # make colors for plot
        colorspec = self.make_colorspec(w_hist)
        
        arrows = True
        if 'arrows' in kwargs:
            arrows = kwargs['arrows']

        ### plot function decrease plot in right panel
        for j in range(len(w_hist)):  
            w_val = w_hist[j]

            # plot each weight set as a point
            ax.scatter(w_val[0],w_val[1],s = 80,color = colorspec[j],edgecolor = self.edgecolor,linewidth = 2*math.sqrt((1/(float(j) + 1))),zorder = 3)

            # plot connector between points for visualization purposes
            if j > 0:
                pt1 = w_hist[j-1]
                pt2 = w_hist[j]
                
                # produce scalar for arrow head length
                pt_length = np.linalg.norm(pt1 - pt2)
                head_length = 0.1
                alpha = (head_length - 0.35)/pt_length + 1
                
                # if points are different draw error
                if np.linalg.norm(pt1 - pt2) > head_length and arrows == True:
                    if np.ndim(pt1) > 1:
                        pt1 = pt1.flatten()
                        pt2 = pt2.flatten()
                        
                        
                    # draw color connectors for visualization
                    w_old = pt1
                    w_new = pt2
                    ax.plot([w_old[0],w_new[0]],[w_old[1],w_new[1]],color = colorspec[j],linewidth = 2,alpha = 1,zorder = 2)      # plot approx
                    ax.plot([w_old[0],w_new[0]],[w_old[1],w_new[1]],color = 'k',linewidth = 3,alpha = 1,zorder = 1)      # plot approx
                
# 16 April: added formula of conic section and plotting it
# plotting simply planet's current position, not previous positions
# adding eccentricity, and semi major and minor axes
# now trying to add kinetic, potential, and total energy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def solution(xi,xti,yi,yti,tt):
    # (xi,xt1,yi,yti,tt) =


    dt = 0.01

    n_time = int(tt/dt) + 1

    zeit = np.linspace(0,tt,n_time) # size of this array is n_time
    dt = zeit[1] - zeit[0]

    n_var = 4
    xvar = np.zeros((n_var,n_time))

    #############################################################
    # convert initial x, xdot etc. to r, rdot, theta, thetadot
    r0    = np.sqrt(xi*xi+yi*yi)
    if xi>=0.0 and yi>=0.0:
        phi0  = np.arctan(yi/xi)
    if xi<=0.0 and yi<=0.0:
        phi0  = np.arctan(yi/xi) + np.pi
    if xi>=0.0 and yi<=0.0:
        phi0  = np.arctan(yi/xi)    
    if xi<=0.0 and yi>=0.0:
        phi0  = np.arctan(yi/xi) + np.pi   

    rt0   = xti*np.cos(phi0) + yti*np.sin(phi0)
    phit0 = (-xti*np.sin(phi0) + yti*np.cos(phi0))/r0
    # 16 April: formula of conic section
    beta = 1.0/((r0**4.0)*(phit0**2.0))
    trm1 = (1.0/r0)-beta
    trm2 = rt0/(r0*r0*phit0)
    trm3 = (r0 - (r0*r0*beta))*phit0
    s0  = np.sqrt((trm1*trm1)+(trm2*trm2))
    th0 = phi0 - np.arctan(rt0/trm3)
    #check on which conic the initial point lies
    r_test = 1.0 / (beta + s0*np.cos(phi0-th0))
    if abs(r_test-r0)<0.0000005:
        sig = 1.0
    r_test = 1.0 / (beta - s0*np.cos(phi0-th0))
    if abs(r_test-r0)<0.0000005:
        sig = -1.0
    # there is still a potential bug lurking here:
    # it could happen that the initial point is shared by both the conics
    #############################################################

    xvar[0,0] = r0  #initial r
    xvar[1,0] = rt0 #initial rdot
    xvar[2,0] = phi0  #initial theta
    xvar[3,0] = phit0 #initial thetadot



    for ii in range(n_time-1):
        xvar[:,ii+1] = rk4(xvar[:,ii],dt,n_var)

    df_1 = xvar[0,:]
    df_2 = xvar[1,:]
    df_3 = xvar[2,:]
    df_4 = xvar[3,:]

    # convert back to rectangular coordinates:
    df_x = df_1*np.cos(df_3)
    df_y = df_1*np.sin(df_3)

    # making the animation----------

    
    make_animation(zeit,df_x,df_y,s0,th0,beta,sig)


    #################################


#############################################################

# ss0, the0 and bbt are the parameters for the ellipse
def make_animation(zt,d1,d2,ss0,the0,bbt,sign):
    nzt = zt.size
    minval1 = min(d1)
    minval2 = min(d2)
    minval  = min(minval1,minval2)
    maxval1 = max(d1)
    maxval2 = max(d2)
    maxval  = max(maxval1,maxval2)
    fig = plt.figure()
    ax  = plt.axes(xlim=(1.1*minval,1.1*maxval) , ylim=(1.1*minval,1.1*maxval))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    #ax.grid(True,which="both")
    #ax.patch.set_facecolor('black')


    # setting text for eccentricity, semi major and minor axes
    e = ss0/bbt
    ax.text(minval,maxval,"e = %.4f" % e)#eccentricity = ss0/bbt
    if (e<1.0):
        a = bbt/((bbt*bbt)-(ss0*ss0))
        b = 1.0/np.sqrt((bbt*bbt)-(ss0*ss0))
        ax.text(minval,0.9*maxval,"a = %.4f" % a)#semi major axis
        ax.text(minval,0.8*maxval,"b = %.4f" % b)#semi minor axis
    #############################

    lines = []
    #line1, = ax.plot([],[],lw=2,color="red")
    #lines.append(line1)

    line1 = ax.plot([],[],linestyle="none",marker="o",markersize=6,color="yellow")[0]
    lines.append(line1) #position of sun

    line2 = ax.plot([],[],lw=1,color="black",linestyle="dotted")[0]
    lines.append(line2) #analytical orbit

    line3 = ax.plot([],[],linestyle="none",marker="o",markersize=2,color="red")[0]
    lines.append(line3) #position of planet

    # setting uo dynamic text-------------
    #dyn_text = ax.text(1.0, 0.95, '', transform=ax.transAxes) ###########################################dynamictext
    ######################################







    # calculate the conic section path----------------
    t_ang = np.linspace(0.0,2.0*np.pi,1000)
    # note that the below equation is ambiguous up to + or -ss0
    rcon = 1.0 / (bbt + sign*ss0*np.cos(t_ang-the0)) 
    xcon = rcon*np.cos(t_ang)
    ycon = rcon*np.sin(t_ang)
    #-------------------------------------------------
    # position of sun---------------------------------
    xsun = 0.0
    ysun = 0.0
    x_sun = np.array([xsun])
    y_sun = np.array([ysun])
    #-------------------------------------------------
    

    def init():
        #dyn_text.set_text('') ####################################################dynamictext
        for line in lines:
            line.set_data([],[])
        return lines


    #def init():
    #    line1.set_data([],[])
    #    return line1,

    def animate(i):
        xls = [x_sun,xcon,d1]#d1
        yls = [y_sun,ycon,d2]#d2
        for lnum,line in enumerate(lines):
            if lnum==0:
                line.set_data(xls[lnum], yls[lnum])
            if lnum==1:
                line.set_data(xls[lnum], yls[lnum])
            if lnum==2:
                line.set_data(xls[lnum][i], yls[lnum][i])
        #dyn_text.set_text('time = %.1f' % float(i))#########################################dynamictext
        return lines#,dyn_text ##############################################################dynamictext

        #line1.set_data(xls[:i], yls[:i])
        #return line1,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nzt, interval=5, blit=True)

    #anim.save("anim_03.gif",dpi=80,writer='imagemagick')
    #anim.save('anim03.mp4', fps=120, extra_args=['-vcodec', 'libx264'])

    #plt.legend(loc="upper right",frameon=False)

    plt.show()




#######################################################



def rk4(xi,dt,nvar):

    r      = xi[0]
    rdot   = xi[1]
    phi    = xi[2]
    phidot = xi[3]
    karr = np.zeros((nvar,4))

    karr[0,0] = rdot
    karr[1,0] = (-1.0/(r*r)) + (r*phidot*phidot)
    karr[2,0] = phidot
    karr[3,0] = -2.0*rdot*phidot/r

    r_new       = r      + 0.5*dt*karr[0,0]
    rdot_new    = rdot   + 0.5*dt*karr[1,0]
    phi_new     = phi    + 0.5*dt*karr[2,0]
    phidot_new  = phidot + 0.5*dt*karr[3,0]
    karr[0,1] = rdot_new
    karr[1,1] = (-1.0/(r_new*r_new)) + (r_new*phidot_new*phidot_new)
    karr[2,1] = phidot_new
    karr[3,1] = -2.0*rdot_new*phidot_new/r_new

    r_new       = r      + 0.5*dt*karr[0,1]
    rdot_new    = rdot   + 0.5*dt*karr[1,1]
    phi_new     = phi    + 0.5*dt*karr[2,1]
    phidot_new  = phidot + 0.5*dt*karr[3,1]
    karr[0,2] = rdot_new
    karr[1,2] = (-1.0/(r_new*r_new)) + (r_new*phidot_new*phidot_new)
    karr[2,2] = phidot_new
    karr[3,2] = -2.0*rdot_new*phidot_new/r_new

    r_new       = r      + dt*karr[0,2]
    rdot_new    = rdot   + dt*karr[1,2]
    phi_new     = phi    + dt*karr[2,2]
    phidot_new  = phidot + dt*karr[3,2]
    karr[0,3] = rdot_new
    karr[1,3] = (-1.0/(r_new*r_new)) + (r_new*phidot_new*phidot_new)
    karr[2,3] = phidot_new
    karr[3,3] = -2.0*rdot_new*phidot_new/r_new

    k_a = (karr[:,0] + 2.0*karr[:,1] + 2.0*karr[:,2] + karr[:,3])/6.0

    xnext = xi + dt*k_a

    return xnext

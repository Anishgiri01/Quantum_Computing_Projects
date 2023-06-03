MODULE GVAR
      implicit none
      integer, parameter :: N_particle=2
      integer :: iseed
      real*8, dimension(:,:), allocatable :: r,rm,rp
      real*8, parameter :: h2m=0.5d0,h=0.001d0,step=0.5d0,lambda=0.5d0
      real*8 :: b, z

      contains

      subroutine mcwalk(naccept,wfold,b,z)
      implicit none
      real*8, intent(in)                       :: b, z
      integer, parameter                       :: ntherm=10
      integer                                  :: naccept,i,k,itherm
      real*8                                   :: wfnew,wfold,rn

      naccept=0
      do itherm=1,ntherm
!     attempt to move 
      do i=1,N_particle
        do k=1,3
            call random_number(rn)
            rp(k,i)=r(k,i)+step*(rn-0.5d0)
          end do
        end do
        wfnew=wave_fun(rp,b,z)
!     metropolis:
        call random_number(rn)
        if((wfnew/wfold)**2.ge.rn) then
!     accepted:
          naccept=naccept+1
          r=rp
          wfold=wfnew 
        endif
      end do

      end subroutine mcwalk


      subroutine elocal(energy,b,z)
      implicit none
      real*8, intent(out)                      :: energy
      real*8, intent(in)                       :: b, z
      
      real*8                       :: p(N_particle,N_particle)
      integer                      :: i,j,k
      real*8                       :: r2,wfold,wfm,wfp,ekin,epot,rr,d
      real*8,external              :: vpot

      wfold=wave_fun(r,b,z)
        rp=r
        rm=r

      ekin=0.d0
      do 40 i=1,N_particle
        do 30 k=1,3
        rm(k,i)=r(k,i)-h
        rp(k,i)=r(k,i)+h
        wfp=wave_fun(rp,b,z)
        wfm=wave_fun(rm,b,z)
        ekin=ekin+(wfp+wfm-2.d0*wfold)/h**2
        rp(k,i)=r(k,i)
        rm(k,i)=r(k,i)
 30    continue
 40   continue

  epot=0.d0
  do i=1,N_particle
    rr=sqrt(r(1,i)**2+r(2,i)**2+r(3,i)**2)
    epot=epot-2.d0/rr
  end do
  do i=1,N_particle
    do j=i+1,N_particle
      rr=sqrt((r(1,i)-r(1,j))**2+(r(2,i)-r(2,j))**2+(r(3,i)-r(3,j))**2)
      epot=epot+1.d0/rr
    end do
  end do

  d=0.d0
  do i=1,n_particle
    d=d+lambda*r(1,i)+lambda*r(2,i)
  end do
  epot=epot+0.5d0*d**2

!      write(6,*)ekin,epot,wfold  

      energy=(-h2m*ekin/wfold+epot)

      return
      end    subroutine elocal


      function wave_fun(p,b,z)
      implicit none

      real*8,dimension(:,:)         :: p
      real*8                        :: wave_fun,rrr,r2x,r2y,r2z,r2,r1,r4,r3,jf,rij
      real*8                        :: d12,d34,phi11,phi21,phi12,phi22,phi13,phi23,phi14,phi24, &
&                                      n1,n2,n3,xi1,xi2,xi3,c11,c12,c13,c21,c22,c23,a
      integer                       :: i,j,k,ij,spin(4)
      real*8, intent(in)            :: b, z

!     wave function
      
      wave_fun=0.d0
      ij=0
      a=0.5d0
      jf=1.d0
      do i=1,N_particle-1      
       do j=i+1,N_particle
         ij=ij+1
         r2x=(p(1,i)-p(1,j))**2
         r2y=(p(2,i)-p(2,j))**2
         r2z=(p(3,i)-p(3,j))**2
         rij=sqrt(r2x+r2y+r2z)
         jf=jf*exp(a*rij/(1.d0+b*rij))
       end do
     end do

      r1=sqrt(p(1,1)**2+p(2,1)**2+p(3,1)**2)
      r2=sqrt(p(1,2)**2+p(2,2)**2+p(3,2)**2)

      wave_fun=exp(-1*z*(r1+r2))*jf

      return 
      end function wave_fun
           
      END MODULE GVAR
          
PROGRAM MC      
      USE GVAR
      implicit none

      integer, parameter :: nmoves=100000
      integer :: naccept,idm,k,i,imoves,iaccept, ib, iz
      real*8 :: sume,sume2,wfnew,wfold, e, energy,e2,rn
      real*8, parameter :: b_start = 0.0, b_end = 3.0, b_step = 0.1
      real*8, parameter :: z_start = 0.0, z_end = 3.0, z_step = 0.1

      allocate(r(3,N_particle),rp(3,N_particle),rm(3,N_particle))
      iseed=-12315

      open(unit=10, file="output.txt")

      do ib = 0, nint((b_end - b_start) / b_step)
        b = b_start + ib * b_step
        do iz = 0, nint((z_end - z_start) / z_step)
        z = z_start + iz * z_step
              naccept=0
              sume=0.d0
              sume2=0.d0
              wfnew=0.d0
              wfold=1.d-50

              do i=1,N_particle
                  do k=1,3
                    call random_number(rn)
                    r(k,i)=step*(rn-0.5d0)
                  end do
              end do
              idm=0

              do imoves=1,nmoves
                  call mcwalk(iaccept, wfold, b, z)
                  naccept=naccept+iaccept
                  call elocal(energy, b, z)
                  sume=sume+energy
                  sume2=sume2+energy**2
                  idm=idm+1
                  if(idm.eq.5000) then
                      idm=0
                      e=sume/imoves
                      e2=sume2/imoves
                  endif
              end do

              e=sume/nmoves
              e2=sume2/nmoves

              write(10,*) b, z, e
          end do
      end do
      close(10)
      deallocate(r,rm,rp)
      
      end PROGRAM MC
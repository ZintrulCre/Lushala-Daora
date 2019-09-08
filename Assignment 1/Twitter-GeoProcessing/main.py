import sys
sys.path.append('./')

exec(open("MultiThread.py").read())
# exec(open("MultiProcess/MultiProcess.py").read())
# exec(open("MultiNode.py").read())

# from mpi4py import MPI
# import random
#
# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()
#
# if rank == 1:
#     for i in range(10):
#         m = random.random()
#         comm.isend(m, dest=0, tag=i)
#         print("rank 1 send", str(m))
# else:
#     for i in range(10):
#         m = comm.irecv(source=1, tag=i)
#         print("rank 0 recv", str(m))

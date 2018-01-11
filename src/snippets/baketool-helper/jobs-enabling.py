import bpy

startJob = 0
endJob = 6
device = "GPU"
wantedSamples = 2048

D = bpy.data

print("+++++ BAKETOOL HELPER +++++")
print("{} existing jobs".format(len(D.scenes[0].BakeTool_Jobs.Jobs)))
        
def resetAllBakeToolJobs():
    for job in range(len(D.scenes[0].BakeTool_Jobs.Jobs)):
        D.scenes[0].BakeTool_Jobs.Jobs[job].enabled = False
    print("all jobs disabled")
    
def setBakeToolJobsEnable():
    if endJob <= len(D.scenes[0].BakeTool_Jobs.Jobs):
        for job in range(startJob, endJob):
            D.scenes[0].BakeTool_Jobs.Jobs[job].enabled = True
            print("job {} enabled".format(job))
            
def setBakeToolJobsSamples():
    for job in range(len(D.scenes[0].BakeTool_Jobs.Jobs)):
        D.scenes[0].BakeTool_Jobs.Jobs[job].job_pass.Pass[0].samples = wantedSamples
    print("samples set to {}".format(wantedSamples))
    
def setBakeToolJobsDevice():
    for job in range(len(D.scenes[0].BakeTool_Jobs.Jobs)):
        D.scenes[0].BakeTool_Jobs.Jobs[job].job_pass.Pass[0].render_device = device
    print("device set to {}".format(device))

resetAllBakeToolJobs()
#setBakeToolJobsEnable()
#setBakeToolJobsSamples()
#setBakeToolJobsDevice()
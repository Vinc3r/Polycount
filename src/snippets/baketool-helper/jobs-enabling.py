import bpy

startJob = 6
endJob = 8

D = bpy.data

print("+++++ BAKETOOL HELPER +++++")
print(str(len(D.scenes[0].BakeTool_Jobs.Jobs))+" jobs sets")
        
def resetAllBakeToolJobs():
    for job in range(len(D.scenes[0].BakeTool_Jobs.Jobs)):
        D.scenes[0].BakeTool_Jobs.Jobs[job].enabled = False
    
def setBakeToolJobsEnable():
    if endJob < len(D.scenes[0].BakeTool_Jobs.Jobs):
        for job in range(startJob, endJob):
            D.scenes[0].BakeTool_Jobs.Jobs[job].enabled = True

resetAllBakeToolJobs()

#setBakeToolJobsEnable()
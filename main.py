from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Create FastAPI application
app = FastAPI(
    title="Course Enrollment API",
    description="Simple API for students and courses",
    version="1.0"
)


# -------------------------
# Data
# -------------------------

courses = []
students = [
    {"id": 1, "name": "Arif"},
    {"id": 2, "name": "Rahul"},
    {"id": 3, "name": "Priya"}
]

enrollments = []


# -------------------------
# Request Models
# -------------------------

class Course(BaseModel):
    name: str
    instructor: str


class Enrollment(BaseModel):
    student_id: int
    course_id: int


# -------------------------
# POST /courses
# Create Course
# -------------------------

@app.post("/courses")
def create_course(course: Course):

    new_course = {
        "id": len(courses) + 1,
        "name": course.name,
        "instructor": course.instructor
    }

    courses.append(new_course)

    return {
        "message": "Course created successfully",
        "course": new_course
    }


# -------------------------
# GET /courses
# Get All Courses
# -------------------------

@app.get("/courses")
def get_courses():

    return {
        "courses": courses
    }


# -------------------------
# POST /enroll
# Enroll Student
# -------------------------

@app.post("/enroll")
def enroll_student(enrollment: Enrollment):

    # Check student
    student = next(
        (s for s in students if s["id"] == enrollment.student_id),
        None
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check course
    course = next(
        (c for c in courses if c["id"] == enrollment.course_id),
        None
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Check duplicate enrollment
    for existing in enrollments:
        if (
            existing["student_id"] == enrollment.student_id
            and existing["course_id"] == enrollment.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student is already enrolled in this course"
            )

    # Create enrollment
    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enrollment successful",
        "enrollment": new_enrollment
    }


# -------------------------
# GET /students/{student_id}/courses
# Get Student Courses
# -------------------------

@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int):

    # Check student
    student = next(
        (s for s in students if s["id"] == student_id),
        None
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student_courses = []

    for enrollment in enrollments:

        if enrollment["student_id"] == student_id:

            course = next(
                (
                    c for c in courses
                    if c["id"] == enrollment["course_id"]
                ),
                None
            )

            if course:
                student_courses.append(course)

    return {
        "student": student,
        "courses": student_courses
    }


# -------------------------
# DELETE /enroll/{enrollment_id}
# Delete Enrollment
# -------------------------

@app.delete("/enroll/{enrollment_id}")
def delete_enrollment(enrollment_id: int):

    enrollment = next(
        (
            e for e in enrollments
            if e["id"] == enrollment_id
        ),
        None
    )

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    enrollments.remove(enrollment)

    return {
        "message": "Enrollment deleted successfully"
    }
"""
    Project Name: Catalog App
    File: createSampleDB creates a new db with sample data
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
from sqlalchemy import func

from catalog.model import User, Category, Item
from catalog.dbConnect import dbConnect

# Load sample data into a newly created DB
def dbLoad():
    dbSession = dbConnect()

    # Make sure the database is empty before running this inital data load.
    category_count = dbSession.query(func.count(Category.id)).scalar()
    if dbSession.query(func.count(Category.id)).scalar() > 0:
        dbSession.close()
        return
    
    # Create default user for items
    user = User(name="Stephen Harris", email="stephennharris@bellsouth.net")
    dbSession.add(user)
    dbSession.commit()

    # Create 12 categories of programming languages.
    sampleCategory1 = Category(name="Procedural languages")
    sampleCategory2 = Category(name="Machine languages")
    sampleCategory3 = Category(name="Interpreted languages")
    sampleCategory4 = Category(name="Numerical Analysis")
    sampleCategory5 = Category(name="Assembly languages")
    sampleCategory6 = Category(name="Authoring languages")
    sampleCategory7 = Category(name="Compiled languages")
    sampleCategory8 = Category(name="Array Languages")
    sampleCategory9 = Category(name="Embeddable languages")
    sampleCategory10 = Category(name="Functional languages")
    sampleCategory11= Category(name="Declarative languages")
    sampleCategory12= Category(name="Concurrent languages")

    dbSession.add(sampleCategory1)
    dbSession.add(sampleCategory2)
    dbSession.add(sampleCategory3)
    dbSession.add(sampleCategory4)
    dbSession.add(sampleCategory5)
    dbSession.add(sampleCategory6)
    dbSession.add(sampleCategory7)
    dbSession.add(sampleCategory8)
    dbSession.add(sampleCategory9)
    dbSession.add(sampleCategory10)
    dbSession.add(sampleCategory11)
    dbSession.add(sampleCategory12)

    dbSession.commit()

    # Create 2 items/category
    dbSession.add(Item(
        user=user,
        category=sampleCategory1,
        name="Ada",
        description=(
            "Ada is a structured, statically typed, imperative, and object-oriented high-level"
            "computer programming language, extended from Pascal and other languages. It has "
            "built-in language support for design-by-contract, extremely strong typing, explicit "
            "concurrency, tasks, synchronous message passing, protected objects, and non-determinism. "
            "Ada improves code safety and maintainability by using the compiler to find errors in "
            "favor of runtime errors."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory1,
        name="Basic",
        description=(
            "BASIC (an acronym for Beginner's All-purpose Symbolic Instruction Code)[2] is a family "
            "of general-purpose, high-level programming languages whose design philosophy emphasizes "
            "ease of use. In 1964, John G. Kemeny and Thomas E. Kurtz designed the original BASIC language "
            "at Dartmouth College. They wanted to enable students in fields other than science and "
            "mathematics to use computers. At the time, nearly all use of computers required writing custom "
            "software, which was something only scientists and mathematicians tended to learn."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory2,
        name="68000X",
        description=(
            "The Motorola 68000 series (also termed 680x0, m68000, m68k, or 68k) is a family of 32-bit CISC "
            "microprocessors. During the 1980s and early 1990s, they were popular in personal computers and "
            "workstations and were the primary competitors of Intel's x86 microprocessors. They were most well "
            "known as the processors powering the early Apple Macintosh, the Commodore Amiga, the Sinclair QL, "
            "the Atari ST, the Sega Genesis (Mega Drive), and several others. Although no modern desktop "
            "computers are based on processors in the 68000 series, derivative processors are still widely "
            "used in embedded systems."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory2,
        name="ARM",
        description=(
            "ARM, previously Advanced RISC Machine, originally Acorn RISC Machine, is a family of reduced "
            "instruction set computing (RISC) architectures for computer processors, configured for various "
            "environments. Arm Holdings develops the architecture and licenses it to other companies, who "
            "design their own products that implement one of those architectures including systems on chips"
            "(SoC) and systems-on-modules (SoM) that incorporate memory, interfaces, radios, etc. It also "
            "designs cores that implement this instruction set and licenses these designs to a number of companies "
            "that incorporate those core designs into their own products."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory3,
        name="Python",
        description=(
            "Python is an interpreted, high-level, general-purpose programming language. Created by Guido van "
            "Rossum and first released in 1991, Python has a design philosophy that emphasizes code readability, "
            "notably using significant whitespace. It provides constructs that enable clear programming on both "
            "small and large scales.[26] In July 2018, Van Rossum stepped down as the leader in the language community."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory3,
        name="JavaScript",
        description=(
            "JavaScript often abbreviated as JS, is a high-level, interpreted programming language that conforms "
            "to the ECMAScript specification. It is a language which is also characterized as dynamic, weakly "
            "typed, prototype-based and multi-paradigm."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory4,
        name="R",
        description=(
            "R is a programming language and free software environment for statistical computing and graphics "
            "supported by the R Foundation for Statistical Computing.[6] The R language is widely used among "
            "statisticians and data miners for developing statistical software[7] and data analysis.[8] Polls, "
            "data mining surveys and studies of scholarly literature databases, show substantial increases in "
            "popularity in recent years.[9] As of December 2018, R ranks 16th in the TIOBE index, a measure of "
            "popularity of programming languages."
        )
    ))

    dbSession.add(Item(
        user=user,
        category=sampleCategory4,
        name="MATLAB",
        description=(
            "MATLAB (matrix laboratory) is a multi-paradigm numerical computing environment and proprietary "
            "programming language developed by MathWorks. MATLAB allows matrix manipulations, plotting of "
            "functions and data, implementation of algorithms, creation of user interfaces, and interfacing "
            "with programs written in other languages, including C, C++, C#, Java, Fortran and Python."
        )
    ))
    dbSession.commit()


if __name__ == '__main__':
    dbLoad()

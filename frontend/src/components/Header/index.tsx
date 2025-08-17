function Header() {
    return (
        <header className="bg-white shadow-sm border-b">
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-1l-4 4z" />
                            </svg>
                        </div>
                        <h1 className="text-xl font-bold text-gray-800">
                            ChatPDF
                        </h1>
                    </div>
                    <nav className="flex items-center space-x-4">
                        <span className="text-sm text-gray-500">
                            AI-Powered PDF Conversations
                        </span>
                    </nav>
                </div>
            </div>
        </header>
    )
}
export default Header;